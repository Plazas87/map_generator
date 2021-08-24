import logging
import re
from typing import Dict

import settings

logger = logging.getLogger(__name__)


def parse_columns(columns: str) -> Dict[str, int]:
    """Parse the columns entered by the user into a dict."""
    logger.debug("Parsing columns list: %s", columns)
    columns = re.sub(r"([\[ \]])", "", columns).split(",")

    logger.debug("Successfully parsed: %s", columns)
    columns_dict = {
        column_name: int(column)
        for column, column_name in zip(
            columns, settings.DEFAULT_COLUMN_DICT_ORDER.keys()
        )
    }

    return columns_dict
