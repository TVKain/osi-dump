from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class LoadBalancer(BaseModel):
    model_config = ConfigDict(strict=True)

    id: str

    load_balancer_name: Optional[str]

    provisioning_status: Optional[str]

    operating_status: Optional[str]

    amphoraes: list[dict]

    project_id: Optional[str]
