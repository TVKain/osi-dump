from pydantic import BaseModel, ConfigDict, ValidationError


class Hypervisor(BaseModel):
    hypervisor_id: str
    hypervisor_type: str
    name: str
    state: str
    status: str
    local_disk_size: int
    memory_size: int
    vpus: int
