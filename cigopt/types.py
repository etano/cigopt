from pydantic import BaseModel
from typing import Any, Dict, List, Union
from uuid import uuid4 as uuid


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
    experiment_id: str = str(uuid())
    results: List[Result] = []
    best_params: List[Parameter] = []
