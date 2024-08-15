from openstack.connection import Connection
from openstack.identity.v3.service import Service


def get_amphorae(connection: Connection, load_balancer_id: str) -> str | None:

    octavia_endpoint = connection.endpoint_for(
        service_type="octavia", interface="public"
    )

    url = f"{octavia_endpoint}/v2/octavia/amphorae"

    response = connection.session.get(url)

    data = response.json()

    return data["usages"]
