from .mappers import MapBuilder
from .readers import FileReader
import logging


logger = logging.getLogger(__name__)


class MapPlotter:
    def __init__(self, file_name: str, output_file_name: str) -> None:
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
        locations = station_list.iloc[:, [25, 24]].values
        # station_name = station_list.iloc[:, [0]].values

        logger.info("Start adding markers...")
        for location in locations:
            self.map_builder.add_marker(
                location=tuple(location),
                icon_file_name="forecast.png",
            )

        logger.info("Markers successfully added.")

        self.map_builder.add_layer_control()\
            .add_measure_control()

        self.map_builder.save_map(self.output_file_name)


