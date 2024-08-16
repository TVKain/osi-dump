import logging

import concurrent

from openstack.connection import Connection
from openstack.identity.v3.role_assignment import RoleAssignment as OSRoleAssignment

from osi_dump.importer.role_assignment.role_assignment_importer import (
    RoleAssignmentImporter,
)
from osi_dump.model.role_assignment import RoleAssignment

logger = logging.getLogger(__name__)


class OpenStackRoleAssignmentImporter(RoleAssignmentImporter):
    def __init__(self, connection: Connection):
        self.connection = connection

    def import_role_assignments(self) -> list[RoleAssignment]:
        """Import role_assignments information from Openstack

        Raises:
            Exception: Raises exception if fetching role_assignment failed

        Returns:
            list[RoleAssignment]: _description_
        """

        logger.info(
            f"Importing role_assignments for {self.connection.auth['auth_url']}"
        )

        try:
            osrole_assignments: list[OSRoleAssignment] = list(
                self.connection.identity.role_assignments()
            )
        except Exception as e:
            raise Exception(
                f"Can not fetch role_assignments for {self.connection.auth['auth_url']}"
            ) from e

        role_assignments: list[RoleAssignment] = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._get_role_assignment_info, role_assignment)
                for role_assignment in osrole_assignments
            ]
            for future in concurrent.futures.as_completed(futures):
                role_assignments.append(future.result())

        logger.info(f"Imported role_assignments for {self.connection.auth['auth_url']}")

        return role_assignments

    def _get_role_assignment_info(
        self, role_assignment: OSRoleAssignment
    ) -> RoleAssignment:

        user_id = None
        role_id = None

        try:
            user_id = role_assignment.user["id"]
        except Exception as e:
            logger.warning(f"Can not get user id: {e}")

        try:
            role_id = role_assignment.role["id"]
        except Exception as e:
            logger.warning(f"Can not get role id: {e}")

        user_name = None
        role_name = None

        try:
            role_name = self.connection.identity.get_role(
                role_assignment.role["id"]
            ).name

        except Exception as e:
            logger.warning(f"Can not get role name: {e}")

        try:
            user_name = self.connection.identity.get_user(
                role_assignment.user["id"]
            ).name
        except Exception as e:
            logger.warning(f"Can not get user name: {e}")

        role_assignment_ret = RoleAssignment(
            user_id=user_id,
            user_name=user_name,
            role_id=role_id,
            role_name=role_name,
            scope=role_assignment.scope,
        )

        return role_assignment_ret
