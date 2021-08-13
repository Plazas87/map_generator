from .mappers import MapPlotter
from .readers import FileReader
import logging


logger = logging.getLogger(__name__)


class Mapper:
    def __init__(self, file_name: str, output_file_name: str) -> None:
        self.file_name = file_name
        self.output_file_name = output_file_name
        self.file_reader = FileReader()
        self.map = MapPlotter()

    def generate_heatmap(self) -> None:
        # reader.read_csv_file('Station_list.csv')

        # Load the data
        data = self.file_reader.load_csv_file(self.file_name)

        # Get the only de data related to the location o the station
        locations = data.iloc[:, [4, 5]].values

        # Build the map
        self.map.add_traffic_heatmap(locations=locations)
        self.map.generate_map(self.output_file_name)

    def generate_standard_map(self) -> None:
        self.map.initialize_map()

        logger.info("Loading data...")
        self.file_reader.load_csv_file(self.file_name)
        logger.info("Data successfully loaded.")

        station_list = self.file_reader.data
        locations = station_list.iloc[:, [25, 24]].values
        # station_name = station_list.iloc[:, [0]].values

        for location in locations:
            self.map.add_marker(
                location=tuple(location),
                icon_file_name="forecast.png"
            )

        # self.plotter.add_traffic_station_marker(locations=locations)
        self.map.generate_map(self.output_file_name)


