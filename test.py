import numpy as np
from hyperopt import base, fmin, hp, tpe, Trials
from hyperopt.fmin import generate_trials_to_calculate, FMinIter

n_trials = 100

def fn(args):
    return (args['x'] - 3) ** 2

def get_new_points(results, space, rstate, algo=tpe.suggest, n_points=1):
    points = [result['point'] for result in results]
    trials = generate_trials_to_calculate(points)
    trials.refresh()
    domain = base.Domain(
        lambda args: results[points.index(args)]['result'], space)
    FMinIter(algo, domain, trials, rstate=rstate).serial_evaluate()
    new_ids = trials.new_trial_ids(n_points)
    new_points = algo(new_ids, domain, trials, rstate.randint(2 ** 31 - 1))
    return new_points, trials.best_trial if results else None

def test_cigopt():
    seed = 0
    rstate = np.random.RandomState(seed)
    results = []
    for i in range(n_trials):
        new_points, best_trial = get_new_points(
            results=results,
            space={'x': hp.uniform('x', -5, 5)},
            rstate=rstate,
            algo=tpe.suggest)
        for point in new_points:
            args = {k: v[0] for k, v in point['misc']['vals'].iteritems()}
            results.append({'point': args, 'result': fn(args)})
    return best_trial, results

def test_hyperopt():
    seed = 0
    rstate = np.random.RandomState(seed)
    space={'x': hp.uniform('x', -5, 5)}
    trials = Trials()
    best_trial = fmin(
        fn, space, algo=tpe.suggest, max_evals=n_trials, rstate=rstate,
        trials=trials)
    return best_trial, trials

cigopt_best_trial, cigopt_trials = test_cigopt()
hyperopt_best_trial, hyperopt_trials = test_hyperopt()
for cigopt_trial, hyperopt_trial in zip(cigopt_trials, hyperopt_trials):
    assert cigopt_trial['point']['x'] == hyperopt_trial['misc']['vals']['x'][0]
    assert cigopt_trial['result'] == hyperopt_trial['result']['loss']
assert cigopt_best_trial['misc']['vals']['x'][0] == hyperopt_best_trial['x']
