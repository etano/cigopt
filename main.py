import numpy as np
from fastapi import FastAPI
from typing import Dict

from cigopt import get_new_params
from cigopt.types import Experiment, Result


app = FastAPI()
rstate = np.random.RandomState(0)
experiments: Dict[str, Experiment] = {}


@app.post("/experiment")
def create_experiment(experiment: Experiment):
    experiments[experiment.experiment_id] = experiment
    return experiment


@app.get("/experiment/{experiment_id}")
def read_experiment(experiment_id: str):
    assert experiment_id in experiments
    return experiments[experiment_id]


@app.put("/experiment/{experiment_id}")
def update_experiment(experiment_id: str, experiment: Experiment):
    assert experiment_id in experiments
    experiments[experiment_id].update(experiment)
    return experiments[experiment_id]


@app.post("/experiment/{experiment_id}/result")
def update_experiment_results(experiment_id: str, result: Result):
    assert experiment_id in experiments
    experiment = experiments[experiment_id]
    experiment.results.append(result)
    return get_new_params(experiment=experiment, rstate=rstate)
