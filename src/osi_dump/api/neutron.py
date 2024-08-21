import logging

from openstack.connection import Connection
from openstack.identity.v3.service import Service
from openstack.load_balancer.v2.load_balancer import LoadBalancer

import osi_dump.util.openstack_util as os_util

logger = logging.getLogger(__name__)


def get_floating_ip_project(connection: Connection, floating_ip_id: str):
    neutron_endpoint = os_util.get_endpoint(
        connection=connection, service_type="network", interface="public"
    )

    try:
        url = f"{neutron_endpoint}/v2.0/floatingips/{floating_ip_id}?fields=project_id"
        response = connection.session.get(url)

    except Exception as e:
        print(e)

    data = response.json()

    return data["floatingip"]["project_id"]


def get_router_project(connection: Connection, router_id: str):
    neutron_endpoint = os_util.get_endpoint(
        connection=connection, service_type="network", interface="internal"
    )

    try:
        url = f"{neutron_endpoint}/v2.0/routers/{router_id}?fields=project_id"

        response = connection.session.get(url)

    except Exception as e:
        print(e)

    data = response.json()

    return data["router"]["project_id"]
