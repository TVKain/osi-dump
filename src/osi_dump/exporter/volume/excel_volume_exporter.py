import pandas as pd

import logging


from osi_dump import util

from osi_dump.exporter.volume.volume_exporter import VolumeExporter

from osi_dump.model.volume import Volume

logger = logging.getLogger(__name__)


class ExcelVolumeExporter(VolumeExporter):
    def __init__(self, sheet_name: str, output_file: str):
        self.sheet_name = sheet_name
        self.output_file = output_file

    def export_volumes(self, volumes: list[Volume]):
        df = pd.DataFrame([volume.model_dump() for volume in volumes])

        logger.info(f"Exporting volumes for {self.sheet_name}")
        try:
            util.export_data_excel(self.output_file, sheet_name=self.sheet_name, df=df)

            logger.info(f"Exported volumes for {self.sheet_name}")
        except Exception as e:
            logger.warning(f"Exporting volumes for {self.sheet_name} error: {e}")
