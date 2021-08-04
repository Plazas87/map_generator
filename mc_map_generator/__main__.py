from .app import Mapper
import typer


app = typer.Typer()


@app.command()
def heat_map(file_name: str, output_file_name: str = 'heatmap_traffic_station_map') -> None:
    mapper = Mapper(file_name=file_name, output_file_name=output_file_name)
    mapper.generate_heatmap()


@app.command()
def standard_map(file_name: str, output_file_name: str = 'traffic_station_map') -> None:
    mapper = Mapper(file_name=file_name, output_file_name=output_file_name)
    mapper.generate_standard_map()


app()
