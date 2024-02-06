from datetime import UTC, datetime
from typing import ClassVar
from uuid import uuid4

from pydantic import UUID4, BaseModel, ConfigDict, Field


class MongoBaseModel(BaseModel):
    model_config: ClassVar = ConfigDict(
        extra='ignore',
        str_min_length=1,
        str_strip_whitespace=True,
        use_enum_values=True,
        validate_default=True,
        validate_return=True,
    )

    id: UUID4 = Field(default_factory=lambda: uuid4())
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
