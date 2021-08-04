from .mappers import Plotter
from .readers import FileReader


class Mapper:
    def __init__(self, file_name: str, output_file_name: str) -> None:
        self.file_name = file_name
        self.output_file_name = output_file_name
        self.file_reader = FileReader()
        self.plotter = Plotter()

    def generate_heatmap(self) -> None:
        # reader.read_csv_file('Station_list.csv')

        # Load the data
        data = self.file_reader.load_csv_file(self.file_name)

        # Get the only de data related to the location o the station
        locations = data.iloc[:, [4, 5]].values

        # Build the map
        self.plotter.add_traffic_heatmap(locations=locations)
        self.plotter.generate_map(self.output_file_name)

    def generate_standard_map(self) -> None:
        self.file_reader.load_csv_file(self.file_name)
        station_list = self.file_reader.data
        locations = station_list.iloc[:, [4, 5]].values
        station_name = station_list.iloc[:, [0]].values
        self.plotter.add_traffic_station_marker(locations=locations, station_names=station_name)
        self.plotter.generate_map(self.output_file_name)


