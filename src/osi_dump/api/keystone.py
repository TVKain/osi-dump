import logging

from openstack.connection import Connection
from openstack.identity.v3.service import Service
from openstack.load_balancer.v2.load_balancer import LoadBalancer

import osi_dump.util.openstack_util as os_util

logger = logging.getLogger(__name__)


def get_role_assignments(connection: Connection): 
    keystone_endpoints = os_util.get_endpoints(
        connection=connection, service_type="identity", interface="public"
    )
    
    for endpoint in keystone_endpoints: 
        try: 
            url = f"{endpoint}/v3/role_assignments?include_names"
            response = connection.session.get(url)
            if response.status_code == 200: 
                break
        except Exception as e: 
            logger.info(e) 
    
    if response is None: 
        return []
    
    return response.json()['role_assignments']
    