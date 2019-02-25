"""Inverts hyperopt"""


import numpy as np
from hyperopt import base, fmin, hp, tpe, Trials
from hyperopt.fmin import generate_trials_to_calculate, FMinIter


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


def run_cigopt(fn, n_trials):
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


def run_hyperopt(fn, n_trials):
    seed = 0
    rstate = np.random.RandomState(seed)
    space={'x': hp.uniform('x', -5, 5)}
    trials = Trials()
    best_trial = fmin(
        fn, space, algo=tpe.suggest, max_evals=n_trials, rstate=rstate,
        trials=trials)
    return best_trial, trials
