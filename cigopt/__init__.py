from hyperopt import base, hp, tpe
from hyperopt.fmin import generate_trials_to_calculate, FMinIter
from typing import Any, Dict, List

from cigopt.types import Parameter, ParameterSpace, Experiment


def convert_parameter_space(parameter_spaces: List[ParameterSpace]) -> Dict[str, Any]:
    converted_parameter_spaces = {}
    for ps in parameter_spaces:
        space = None
        if ps.space_type == 'uniform':
            space = hp.uniform(ps.parameter_name, ps.space_values['min'], ps.space_values['max'])
        else:
            raise ValueError(f'Unrecognized parameter space type: {ps.space_type}')
        converted_parameter_spaces[ps.parameter_name] = space
    return converted_parameter_spaces


def get_new_params(experiment: Experiment, rstate, algo=tpe.suggest, n_points=1):
    params = [{p.name: p.value for p in result.params} for result in experiment.results]
    trials = generate_trials_to_calculate(params)
    trials.refresh()
    space = convert_parameter_space(experiment.parameter_spaces)
    domain = base.Domain(lambda args: experiment.results[params.index(args)].value, space)
    FMinIter(algo, domain, trials, rstate=rstate).serial_evaluate()
    new_ids = trials.new_trial_ids(n_points)
    new_points = algo(new_ids, domain, trials, rstate.randint(2 ** 31 - 1))
    new_params = [[Parameter(name=k, value=v[0]) for k, v in point['misc']['vals'].items()] for point in new_points]
    if experiment.results:
        experiment.best_params = [Parameter(name=k, value=v) for k, v in trials.best_trial['misc']['vals'].items()]
    return new_params, experiment
