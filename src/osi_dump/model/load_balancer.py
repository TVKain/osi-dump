from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class LoadBalancer(BaseModel):
    model_config = ConfigDict(strict=True)

    id: str

    load_balancer_name: Optional[str]

    status: str

    # amphora_id: Optional[str]

    project_id: Optional[str]
