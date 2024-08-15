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

        try:
            compute_quotas = self.connection.compute.get_quota_set(
                project.id, usage=True
            )
        except Exception as e:
            logger.warning(f"Get compute quotas failed for {project.id} error: {e}")

        try:
            storage_quotas = self.connection.block_storage.get_quota_set(
                project.id, usage=True
            )
        except Exception as e:
            logger.warning(f"Get storage quotas failed for {project.id} error: {e}")

        project_ret = Project(
            project_id=project.id,
            project_name=project.name,
            domain_id=project.domain_id,
            enabled=project.is_enabled,
            parent_id=project.parent_id,
            usage_instance=compute_quotas.usage["instances"],
            quota_instance=compute_quotas.instances,
            usage_ram=compute_quotas.usage["ram"],
            quota_ram=compute_quotas.ram,
            usage_vcpu=compute_quotas.usage["cores"],
            quota_vcpu=compute_quotas.cores,
            usage_volume=storage_quotas.usage["volumes"],
            quota_volume=storage_quotas.volumes,
            usage_snapshot=storage_quotas.usage["snapshots"],
            quota_snapshot=storage_quotas.snapshots,
            usage_storage=storage_quotas.usage["gigabytes"],
            quota_storage=storage_quotas.gigabytes,
        )

        return project_ret
