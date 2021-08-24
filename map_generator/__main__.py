import logging.config
import sys

from .app import MapPlotter
import typer
import yaml
import settings
from .readers import FileReader
from .utils import parse_columns

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
    columns: str = typer.Argument(
        ...,
        help="CSV column numbers as a list, for example: [3,5,6]. You must pay special "
        "attention to the order fo this list. Make sure you keep the following "
        "order: [lat,long,legend,tooltip]. Don't use spaces between the elements of the list.",
    ),
    file_name: str = typer.Option(
        "madrid_air_quality_stations.csv", help="CSV filename to Plot: 'file_name.csv'"
    ),
    output_file_name: str = typer.Option(
        "example_map",
        help="Filename for the resulting Map: 'generated_map_name'. Avoid adding the file "
        "extension at the end, by default the resulting Map is an '*.html' file.",
    ),
) -> None:
    logger.info("Starting...")

    try:
        columns_dict = parse_columns(columns)
    except Exception as e:
        logger.error("Error while parsing the column numbers: %s", e)
        sys.exit(1)

    logger.info("Loading data...")
    file_reader = FileReader()
    data = file_reader.load_csv_file(file_name)

    map_plotter = MapPlotter(
        data=data,
        columns_dict=columns_dict,
        file_name=file_name,
        output_file_name=output_file_name,
    )
    map_plotter.generate_example_map()


app()
