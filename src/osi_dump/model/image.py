from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class Image(BaseModel):
    model_config = ConfigDict(strict=True)

    image_id: str

    disk_format: str
    min_disk: int
    min_ram: int
    image_name: Optional[str]
    owner: str

    properties: Optional[dict]

    protected: bool
    status: str
    size: int
    virtual_size: int
    visibility: str

    created_at: str
    updated_at: str
