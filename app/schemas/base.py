from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class RequestModel(BaseModel, validate_assignment=True):
    model_config: ClassVar = ConfigDict(
        extra='ignore',
        frozen=True,
        str_min_length=1,
        str_strip_whitespace=True,
        use_enum_values=True,
        validate_default=True,
        validate_return=True,
    )


class ResponseModel(RequestModel):
    pass


class ResponseAttrsModel(ResponseModel):
    model_config: ClassVar = ConfigDict(from_attributes=True)
