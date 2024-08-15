from pydantic import BaseModel, ConfigDict, ValidationError


class Hypervisor(BaseModel):
    hypervisor_id: str
    hypervisor_type: str
    name: str
    state: str
    status: str

    vcpus: int
    vcpus_usage: int

    memory_size: int
    memory_usage: int

    local_disk_usage: int
    local_disk_size: int

    vm_count: int
