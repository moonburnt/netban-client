from pydantic import BaseModel
from typing import Any


class APIResponse(BaseModel):
    api_version: str
    error: bool
    # TODO: specific data variants
    data: list | dict
