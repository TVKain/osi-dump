import logging

import concurrent

from openstack.connection import Connection
from openstack.identity.v3.project import Project as OSProject

from osi_dump.importer.project.project_importer import ProjectImporter
from osi_dump.model.project import Project

logger = logging.getLogger(__name__)


class OpenStackProjectImporter(ProjectImporter):
    def __init__(self, connection: Connection):
        self.connection = connection

    def import_projects(self) -> list[Project]:
        """Import projects information from Openstack

        Raises:
            Exception: Raises exception if fetching project failed

        Returns:
            list[Instance]: _description_
        """

        logger.info(f"Importing projects for {self.connection.auth['auth_url']}")

        try:
            osprojects: list[OSProject] = list(self.connection.identity.projects())
        except Exception as e:
            raise Exception(
                f"Can not fetch projects for {self.connection.auth['auth_url']}"
            ) from e

        projects: list[Project] = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._get_project_info, project)
                for project in osprojects
            ]
            for future in concurrent.futures.as_completed(futures):
                projects.append(future.result())

        logger.info(f"Imported projects for {self.connection.auth['auth_url']}")

        return projects

    def _get_project_info(self, project: OSProject) -> Project:
        project_ret = Project(
            project_id=project.id,
            project_name=project.name,
            domain_id=project.domain_id,
            enabled=project.is_enabled,
            parent_id=project.parent_id,
        )

        return project_ret
