import logging
import json
from typing import Generator
from openstack.connection import Connection
from openstack.block_storage.v3.volume import Volume as OSVolume

from osi_dump.importer.volume.volume_importer import VolumeImporter
from osi_dump.model.volume import Volume

logger = logging.getLogger(__name__)


class OpenStackVolumeImporter(VolumeImporter):
    def __init__(self, connection: Connection):
        self.connection = connection
        self.snapshots_by_volume = {}
        self._snapshots_fetched = False

    def _fetch_snapshots(self):
        """Pre-cache all snapshots mapped by volume_id to avoid N+1 REST API calls."""
        if self._snapshots_fetched:
            return

        logger.info(
            f"Pre-caching snapshots for {self.connection.auth['auth_url']}"
        )
        try:
            snapshot_list = self.connection.block_storage.snapshots(
                details=False, all_projects=True
            )
            for snapshot in snapshot_list:
                vol_id = getattr(snapshot, "volume_id", None)
                snap_id = getattr(snapshot, "id", None)
                if vol_id and snap_id:
                    self.snapshots_by_volume.setdefault(vol_id, []).append(snap_id)
        except Exception as e:
            logger.warning(
                f"Could not pre-fetch all snapshots at once ({e}). Will fallback to per-volume lookup if needed."
            )

        self._snapshots_fetched = True

    def import_volumes(self) -> Generator[Volume, None, None]:
        logger.info(f"Importing volumes for {self.connection.auth['auth_url']}")
        self._fetch_snapshots()

        try:
            osvolume_iterator = self.connection.block_storage.volumes(
                details=True, all_projects=True
            )
            for volume in osvolume_iterator:
                try:
                    yield self._get_volume_info(volume)
                except Exception as e:
                    vol_id = getattr(volume, "id", "unknown")
                    vol_name = getattr(volume, "name", "unknown")
                    logger.error(
                        f"Error processing volume ID {vol_id} (Name: {vol_name}): {e}"
                    )
                    continue

        except Exception as e:
            logger.error(
                f"Cannot fetch volumes for {self.connection.auth['auth_url']}: {e}"
            )
            return

        logger.info(f"Finished importing volumes for {self.connection.auth['auth_url']}")

    def _get_volume_info(self, volume: OSVolume) -> Volume:
        vol_id = getattr(volume, "id", "")
        vol_name = getattr(volume, "name", None)

        snapshots = self.snapshots_by_volume.get(vol_id)
        if snapshots is None:
            snapshots = []
            try:
                snapshot_list = self.connection.block_storage.snapshots(
                    details=False, all_projects=True, volume_id=vol_id
                )
                snapshots = [getattr(snapshot, "id", "") for snapshot in snapshot_list if getattr(snapshot, "id", None)]
                self.snapshots_by_volume[vol_id] = snapshots
            except Exception as e:
                logger.warning(f"Fetching snapshots failed for {vol_id} error: {e}")

        host_attr = getattr(volume, "host", None)

        image_metadata_dict = {}
        raw_meta = getattr(volume, "volume_image_metadata", None)
        if raw_meta:
            if isinstance(raw_meta, str):
                try:
                    image_metadata_dict = json.loads(raw_meta)
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse volume_image_metadata for volume {vol_id}")
            elif isinstance(raw_meta, dict):
                image_metadata_dict = raw_meta

        raw_attachments = getattr(volume, "attachments", []) or []
        attachment_server_ids = []
        for att in raw_attachments:
            if isinstance(att, dict) and "server_id" in att:
                attachment_server_ids.append(str(att["server_id"]))
            elif hasattr(att, "server_id") and att.server_id:
                attachment_server_ids.append(str(att.server_id))

        return Volume(
            volume_id=str(vol_id),
            volume_name=str(vol_name) if vol_name is not None else None,
            project_id=str(volume.project_id) if getattr(volume, "project_id", None) is not None else None,
            user_id=str(volume.user_id) if getattr(volume, "user_id", None) is not None else None,
            status=str(getattr(volume, "status", "")),
            attachments=attachment_server_ids,
            type=str(getattr(volume, "volume_type", "") or ""),
            size=int(getattr(volume, "size", 0) or 0),
            snapshots=snapshots,
            host=str(host_attr) if host_attr is not None else None,
            image_metadata=image_metadata_dict,
            updated_at=str(volume.updated_at) if getattr(volume, "updated_at", None) is not None else None,
            created_at=str(volume.created_at) if getattr(volume, "created_at", None) is not None else None,
        )