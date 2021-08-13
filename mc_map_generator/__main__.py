import logging.config
from typing import Dict, Any

from .app import Mapper
import typer
import yaml
import settings


app = typer.Typer()


logger = logging.getLogger(__name__)


def configure_log() -> None:
    with open(settings.LOGGING_FILE_NAME, 'r') as f:
        dict_conf = yaml.safe_load(f)
        logging.config.dictConfig(dict_conf)


@app.command()
def heat_map(file_name: str, output_file_name: str = 'heatmap_traffic_station_map') -> None:
    configure_log()
    mapper = Mapper(file_name=file_name, output_file_name=output_file_name)
    mapper.generate_heatmap()


@app.command()
def standard_map(file_name: str, output_file_name: str = 'traffic_station_map') -> None:
    configure_log()
    logger.info("Start")
    mapper = Mapper(file_name=file_name, output_file_name=output_file_name)
    logger.info("Mapper successfully created")
    mapper.generate_standard_map()


app()
