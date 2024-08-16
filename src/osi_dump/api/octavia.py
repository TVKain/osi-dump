from openstack.connection import Connection
from openstack.identity.v3.service import Service
from openstack.load_balancer.v2.load_balancer import LoadBalancer


def get_load_balancers(connection: Connection) -> list[LoadBalancer]:
    octavia_endpoint = connection.endpoint_for(
        service_type="load-balancer", interface="public"
    )

    url = f"{octavia_endpoint}/v2.0/lbaas/loadbalancers"

    response = connection.session.get(url)

    data = response.json()

    return data["loadbalancers"]


def get_amphoraes(connection: Connection, load_balancer_id: str) -> list[str]:

    octavia_endpoint = connection.endpoint_for(
        service_type="load-balancer", interface="public"
    )

    url = f"{octavia_endpoint}/v2/octavia/amphorae?load_balancer_id={load_balancer_id}&fields=id&fields=compute_id"

    response = connection.session.get(url)

    data = response.json()

    amphoraes = data["amphorae"]

    return [amphorae["compute_id"] for amphorae in amphoraes]
