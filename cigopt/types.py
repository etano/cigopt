from pydantic import BaseModel
from typing import Any, Dict, List, Union


EXPERIMENT_DOC_TYPE = "experiment"


class Parameter(BaseModel):
    name: str
    value: Union[float, int, str]


class ParameterSpace(BaseModel):
    parameter_name: str
    space_type: str
    space_values: Dict[str, Any]


class Result(BaseModel):
    value: float
    params: List[Parameter]


class Experiment(BaseModel):
    name: str
    parameter_spaces: List[ParameterSpace]
    experiment_id: str = None
    results: List[Result] = []
    best_params: List[Parameter] = []


class ExperimentInDB(Experiment):
    type: str = EXPERIMENT_DOC_TYPE
