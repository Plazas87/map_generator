import logging.config

from .app import MapPlotter
import typer
import yaml
import settings


app = typer.Typer()


def configure_log() -> None:
    with open(settings.LOGGING_FILE_NAME, "r") as f:
        dict_conf = yaml.safe_load(f)
        logging.config.dictConfig(dict_conf)


configure_log()
logger = logging.getLogger(__name__)


@app.command()
def heat_map(
    file_name: str, output_file_name: str = "heatmap_traffic_station_map"
) -> None:
    configure_log()
    map_plotter = MapPlotter(file_name=file_name, output_file_name=output_file_name)
    map_plotter.generate_heatmap()


@app.command()
def example_map(
    file_name: str = typer.Option(
        "madrid_air_quality_stations.csv", help="CSV filename to Plot: 'file_name.csv'"
    ),
    output_file_name: str = typer.Option(
        "madrid_air_quality_stations",
        help="Filename for the resulting Map: 'generated_map_name'. Avoid adding the file "
        "extension at the end, by default the resulting Map is an '*.html' file.",
    ),
) -> None:
    logger.info("Starting...")
    map_plotter = MapPlotter(file_name=file_name, output_file_name=output_file_name)
    map_plotter.generate_example_map()


app()
