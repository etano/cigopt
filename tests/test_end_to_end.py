import numpy as np
import pytest
from hyperopt import fmin, hp, tpe, Trials

from cigopt import get_new_params
from cigopt.types import ParameterSpace, Experiment, Result


def run_cigopt(fn, n_trials):
    experiment = Experiment(
        name='test',
        parameter_spaces=[ParameterSpace(
            parameter_name='x',
            space_type='uniform',
            space_values={
                'min': -5,
                'max': 5
            }
        )]
    )
    seed = 0
    rstate = np.random.RandomState(seed)
    for i in range(n_trials):
        new_params, experiment = get_new_params(
            experiment=experiment,
            rstate=rstate,
            algo=tpe.suggest)
        for params in new_params:
            param_dict = {p.name: p.value for p in params}
            experiment.results.append(Result(value=fn(param_dict), params=params))
    return experiment.best_params, experiment.results


def run_hyperopt(fn, n_trials):
    seed = 0
    rstate = np.random.RandomState(seed)
    space = {'x': hp.uniform('x', -5, 5)}
    trials = Trials()
    best_trial = fmin(
        fn, space, algo=tpe.suggest, max_evals=n_trials, rstate=rstate,
        trials=trials)
    return best_trial, trials


fn_cases = {
    'quadratic': (
        lambda args: (args['x'] - 3) ** 2,
        100
    ),
}
@pytest.mark.parametrize("fn,n_trials", fn_cases.values(), ids=list(fn_cases.keys()))
def test_fn(fn, n_trials):
    cigopt_best_trial, cigopt_trials = run_cigopt(fn, n_trials)
    hyperopt_best_trial, hyperopt_trials = run_hyperopt(fn, n_trials)
    for cigopt_trial, hyperopt_trial in zip(cigopt_trials, hyperopt_trials):
        assert cigopt_trial.params[0].value == hyperopt_trial['misc']['vals']['x'][0]
        assert cigopt_trial.value == hyperopt_trial['result']['loss']
    assert cigopt_best_trial[0].value == hyperopt_best_trial['x']
