import logging

import concurrent

from openstack.connection import Connection
from openstack.compute.v2.hypervisor import Hypervisor as OSHypervisor
from openstack.compute.v2.aggregate import Aggregate as OSAggregate

from openstack.placement.v1._proxy import Proxy as PlacementProxy
from openstack.placement.v1.resource_provider_inventory import ResourceProviderInventory

from osi_dump.importer.hypervisor.hypervisor_importer import HypervisorImporter
from osi_dump.model.hypervisor import Hypervisor

from osi_dump.api.placement import get_usage

logger = logging.getLogger(__name__)


class OpenStackHypervisorImporter(HypervisorImporter):
    def __init__(self, connection: Connection):
        self.connection = connection

    def import_hypervisors(self) -> list[Hypervisor]:
        """Import hypervisors information from Openstack

        Raises:
            Exception: Raises exception if fetching hypervisor failed

        Returns:
            list[Hypervisor]: _description_
        """
        aggregates = list(self.connection.list_aggregates())

        try:
            oshypervisors: list[OSHypervisor] = list(
                self.connection.compute.hypervisors(details=True, with_servers=True)
            )

        except Exception as e:
            raise Exception(
                f"Can not fetch hypervisor for {self.connection.auth['auth_url']}"
            ) from e

        hypervisors: list[Hypervisor] = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._get_hypervisor_info, hypervisor, aggregates)
                for hypervisor in oshypervisors
            ]
            for future in concurrent.futures.as_completed(futures):
                hypervisors.append(future.result())

        logger.info(f"Imported hypervisors for {self.connection.auth['auth_url']}")

        return hypervisors

    def _get_hypervisor_info(
        self, hypervisor: OSHypervisor, aggregates: list[OSAggregate]
    ) -> Hypervisor:
        aggregate = self._get_aggregate(hypervisor=hypervisor)

        aggregate_id = None
        aggregate_name = None
        availability_zone = None

        if aggregate:
            aggregate_id = aggregate.id
            aggregate_name = aggregate.name
            availability_zone = aggregate.availability_zone

        placement_proxy: PlacementProxy = self.connection.placement

        rpi: ResourceProviderInventory = list(
            placement_proxy.resource_provider_inventories(
                resource_provider=hypervisor.id
            )
        )

        usage_data = get_usage(self.connection, resource_provider_id=hypervisor.id)

        vcpu = rpi[0]
        memory = rpi[1]
        disk = rpi[2]

        ret_hypervisor = Hypervisor(
            hypervisor_id=hypervisor.id,
            hypervisor_type=hypervisor.hypervisor_type,
            name=hypervisor.name,
            state=hypervisor.state,
            status=hypervisor.status,
            local_disk_size=disk["max_unit"],
            memory_size=memory["max_unit"] + memory["reserved"],
            vcpus=vcpu["max_unit"],
            vcpus_usage=usage_data["VCPU"],
            memory_usage=usage_data["MEMORY_MB"],
            local_disk_usage=usage_data["DISK_GB"],
            vm_count=len(hypervisor.servers),
            aggregate_id=aggregate_id,
            aggregate_name=aggregate_name,
            availability_zone=availability_zone,
        )

        return ret_hypervisor

    def _get_aggregate(self, hypervisor: OSHypervisor) -> OSAggregate:
        aggregates = list(self.connection.list_aggregates())

        for aggregate in aggregates:
            if hypervisor.name in aggregate.hosts:
                return aggregate

        return None
