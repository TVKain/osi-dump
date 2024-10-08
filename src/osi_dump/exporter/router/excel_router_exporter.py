import pandas as pd

import logging

from openpyxl import load_workbook

from osi_dump import util
from osi_dump.exporter.router.router_exporter import RouterExporter

from osi_dump.model.router import Router

logger = logging.getLogger(__name__)


class ExcelRouterExporter(RouterExporter):
    def __init__(self, sheet_name: str, output_file: str):
        self.sheet_name = sheet_name
        self.output_file = output_file

    def export_routers(self, routers: list[Router]):

        df = pd.DataFrame([router.model_dump() for router in routers])

        logger.info(f"Exporting routers for {self.sheet_name}")
        try:
            util.export_data_excel(self.output_file, sheet_name=self.sheet_name, df=df)

            logger.info(f"Exported routers for {self.sheet_name}")
        except Exception as e:
            logger.warning(f"Exporting routers for {self.sheet_name} error: {e}")
