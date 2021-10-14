import logging
from typing import TYPE_CHECKING, Dict, Optional, Tuple

import settings

from .mappers import FoliumMapBuilder

if TYPE_CHECKING:
    from pandas.core.frame import DataFrame


logger = logging.getLogger(__name__)


class MapPlotter:
    def __init__(
        self,
        data: "DataFrame",
        columns_dict: Dict[str, int],
        file_name: str,
        output_file_name: str,
        icon_filename: Optional[str] = None,
        icon_size: Optional[Tuple[int, int]] = None,
    ) -> None:
        self._data = data
        self._columns_dict = columns_dict
        self.file_name = file_name
        self._icon_filename = icon_filename
        self._icon_size = icon_size
        self.output_file_name = output_file_name
        self.map_builder = FoliumMapBuilder()

    def generate_example_map(self) -> None:
        # Create an empty map
        self.map_builder.initialize_map()

        rows = self._data.iloc[:, list(self._columns_dict.values())].values

        logger.info("Start adding markers...")

        for row in rows:
            dict_row = {
                field_name: row_field
                for row_field, field_name in zip(row, self._columns_dict.keys())
            }

            coordinates = (dict_row[settings.LATITUDE], dict_row[settings.LONGITUDE])

            self.map_builder.add_marker(
                coordinates=coordinates,
                legend=dict_row.get(settings.LEGEND),
                tooltip_text=dict_row.get(settings.TOOLTIP),
                icon_file_name=self._icon_filename,
                icon_size=self._icon_size,
            )

        logger.info("Markers successfully added.")

        self.map_builder.add_layer_control().add_measure_control()

        self.map_builder.save_map(self.output_file_name)
