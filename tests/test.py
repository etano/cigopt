import pytest
from cigopt import run_cigopt, run_hyperopt


fn_cases = {
    'quadratic': (
        lambda args: (args['x'] - 3) ** 2,
        100
    ),
}
@pytest.mark.parametrize("fn,n_trials", fn_cases.values(), ids=fn_cases.keys())
def test_fn(fn, n_trials):
    cigopt_best_trial, cigopt_trials = run_cigopt(fn, n_trials)
    hyperopt_best_trial, hyperopt_trials = run_hyperopt(fn, n_trials)
    for cigopt_trial, hyperopt_trial in zip(cigopt_trials, hyperopt_trials):
        assert cigopt_trial['point']['x'] == \
            hyperopt_trial['misc']['vals']['x'][0]
        assert cigopt_trial['result'] == hyperopt_trial['result']['loss']
    assert cigopt_best_trial['misc']['vals']['x'][0] == hyperopt_best_trial['x']
