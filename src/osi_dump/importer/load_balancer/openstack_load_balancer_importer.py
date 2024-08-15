import logging

import concurrent

from openstack.connection import Connection

from openstack.load_balancer.v2.load_balancer import LoadBalancer as OSLoadBalancer

from osi_dump.importer.load_balancer.load_balancer_importer import (
    LoadBalancerImporter,
)
from osi_dump.model.load_balancer import LoadBalancer

logger = logging.getLogger(__name__)


class OpenStackLoadBalancerImporter(LoadBalancerImporter):
    def __init__(self, connection: Connection):
        self.connection = connection

    def import_load_balancers(self) -> list[LoadBalancer]:
        """Import load_balancers information from Openstack

        Raises:
            Exception: Raises exception if fetching load_balancer failed

        Returns:
            list[LoadBalancer]: _description_
        """

        logger.info(f"Importing load_balancers for {self.connection.auth['auth_url']}")

        try:
            osload_balancers: list[OSLoadBalancer] = list(
                self.connection.network.load_balancers()
            )
        except Exception as e:
            raise Exception(
                f"Can not fetch load_balancers for {self.connection.auth['auth_url']}"
            ) from e

        load_balancers: list[LoadBalancer] = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._get_load_balancer_info, load_balancer)
                for load_balancer in osload_balancers
            ]
            for future in concurrent.futures.as_completed(futures):
                load_balancers.append(future.result())

        logger.info(f"Imported load_balancers for {self.connection.auth['auth_url']}")

        return load_balancers

    def _get_load_balancer_info(self, load_balancer: OSLoadBalancer) -> LoadBalancer:

        load_balancer_ret = LoadBalancer(
            id=load_balancer.id,
            load_balancer_name=load_balancer.name,
            status=load_balancer.operating_status,
            project_id=load_balancer.project_id,
        )

        return load_balancer_ret
