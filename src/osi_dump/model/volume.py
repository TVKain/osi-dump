from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class Volume(BaseModel):
    model_config = ConfigDict(strict=True)

    volume_id: str

    project_id: Optional[str]

    attachments: Optional[list[str]]

    status: str

    type: str
    size: int

    updated_at: str
    created_at: str
