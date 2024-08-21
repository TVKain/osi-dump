from openstack.connection import Connection
from openstack.identity.v3.service import Service

import osi_dump.util.openstack_util as os_util


def get_usage(connection: Connection, resource_provider_id: str):

    placement_endpoint = os_util.get_endpoint(
        connection=connection, service_type="placement", interface="public"
    )

    url = f"{placement_endpoint}/resource_providers/{resource_provider_id}/usages"

    response = connection.session.get(url)

    data = response.json()

    return data["usages"]
