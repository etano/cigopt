import numpy as np
from fastapi import FastAPI
from typing import List
from uuid import uuid4

from cigopt import get_new_params
from cigopt.db import get_controller
from cigopt.types import Experiment, Parameter, Result


app = FastAPI()
rstate = np.random.RandomState(0)


@app.post("/experiment", response_model=Experiment)
def create_experiment(experiment: Experiment):
    controller = get_controller()
    if not experiment.experiment_id:
        experiment.experiment_id = str(uuid4())
    return controller.create_experiment(experiment)


@app.get("/experiment/{experiment_id}", response_model=Experiment)
def read_experiment(experiment_id: str):
    controller = get_controller()
    return controller.get_experiment(experiment_id)


@app.delete("/experiment/{experiment_id}")
def delete_experiment(experiment_id: str):
    controller = get_controller()
    controller.delete_experiment(experiment_id)


@app.post("/experiment/{experiment_id}/result", response_model=Experiment)
def add_result(experiment_id: str, result: Result):
    controller = get_controller()
    experiment = controller.get_experiment(experiment_id)
    experiment.results.append(result)
    return controller.update_experiment(experiment)


@app.get("/experiment/{experiment_id}/params", response_model=List[Parameter])
def get_params(experiment_id: str):
    controller = get_controller()
    experiment = controller.get_experiment(experiment_id)
    return get_new_params(experiment=experiment, rstate=rstate)
