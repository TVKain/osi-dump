from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class Project(BaseModel):
    model_config = ConfigDict(strict=True)

    project_id: str
    project_name: Optional[str]
    domain_id: Optional[str]
    enabled: bool
    parent_id: Optional[str]
