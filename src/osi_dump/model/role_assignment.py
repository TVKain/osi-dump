from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class RoleAssignment(BaseModel):
    model_config = ConfigDict(strict=True)

    user_id: str

    user_name: Optional[str]

    role_id: str

    role_name: Optional[str]

    scope: Optional[dict]
