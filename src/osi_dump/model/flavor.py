from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class Flavor(BaseModel):
    model_config = ConfigDict(strict=True)

    flavor_id: str

    flavor_name: str

    properties: Optional[dict]

    ram: int
    vcpus: int
    disk: int
    swap: Optional[int]

    public: bool
