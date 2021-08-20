from collections import namedtuple
from typing import Dict

import settings
from .mappers import MapBuilder
from .readers import FileReader
import logging


logger = logging.getLogger(__name__)


class MapPlotter:
    def __init__(
        self, columns_dict: Dict[str, int], file_name: str, output_file_name: str
    ) -> None:
        self._columns_dict = columns_dict
        self.file_name = file_name
        self.output_file_name = output_file_name
        self.file_reader = FileReader()
        self.map_builder = MapBuilder()

    def generate_heatmap(self) -> None:
        # reader.read_csv_file('Station_list.csv')

        # Load the data
        data = self.file_reader.load_csv_file(self.file_name)

        # Get the only de data related to the location o the station
        locations = data.iloc[:, [4, 5]].values

        # Build the map
        self.map_builder.add_traffic_heatmap(locations=locations)
        self.map_builder.save_map(self.output_file_name)

    def generate_example_map(self) -> None:
        self.map_builder.initialize_map()

        logger.info("Loading data...")
        self.file_reader.load_csv_file(self.file_name)
        logger.info("Data successfully loaded.")

        station_list = self.file_reader.data
        rows = station_list.iloc[:, list(self._columns_dict.values())].values

        logger.info("Start adding markers...")

        for row in rows:
            dict_row = {
                field_name: row_field
                for row_field, field_name in zip(row, self._columns_dict.keys())
            }

            ColumnNames = namedtuple("ColumnNames", settings.DEFAULT_COLUMN_DICT_ORDER)
            columns = ColumnNames(*settings.DEFAULT_COLUMN_DICT_ORDER)

            # TODO: change this to create the indexes dynamically based on the settings module.
            coordinates = (dict_row[columns.lat], dict_row[columns.lon])

            self.map_builder.add_marker(
                coordinates=coordinates,
                legend=dict_row.get(columns.legend),
                tooltip_text=dict_row.get(columns.tooltip),
                icon_file_name=settings.DEFAULT_ICON_NAME,
                icon_size=settings.DEFAULT_CUSTOM_ICON_SIZE,
            )

        logger.info("Markers successfully added.")

        self.map_builder.add_layer_control().add_measure_control()

        self.map_builder.save_map(self.output_file_name)
