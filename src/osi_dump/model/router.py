from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class Router(BaseModel):
    model_config = ConfigDict(strict=True)

    router_id: str

    name: Optional[str]

    external_net_id: Optional[str]
    external_net_ip: Optional[str]

    status: str
    project_id: Optional[str]

    created_at: str
    updated_at: str
