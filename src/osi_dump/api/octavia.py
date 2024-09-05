from openstack.connection import Connection
from openstack.identity.v3.service import Service
from openstack.load_balancer.v2.load_balancer import LoadBalancer


import osi_dump.util.openstack_util as os_util


def get_load_balancers(connection: Connection) -> list[LoadBalancer]:
    octavia_endpoint = os_util.get_endpoint(
        connection=connection, service_type="load-balancer", interface="public"
    )

    url = f"{octavia_endpoint}/v2.0/lbaas/loadbalancers"

    response = connection.session.get(url)

    data = response.json()

    return data["loadbalancers"]


def get_amphoraes(connection: Connection, load_balancer_id: str) -> list[dict]:

    octavia_endpoint = os_util.get_endpoint(
        connection=connection, service_type="load-balancer", interface="public"
    )

    url = f"{octavia_endpoint}/v2/octavia/amphorae?load_balancer_id={load_balancer_id}&fields=status&fields=compute_id&fields=compute_flavor"

    response = connection.session.get(url)

    data = response.json()

    amphoraes = data["amphorae"]

    return amphoraes
