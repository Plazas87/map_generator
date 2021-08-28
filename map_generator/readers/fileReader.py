import logging
from typing import TYPE_CHECKING, Optional, Tuple, Dict

import pandas as pd

import settings


if TYPE_CHECKING:
    from pandas.core.frame import DataFrame


logger = logging.getLogger(__name__)


class FileReader:
    def __init__(self):
        self._separators: Dict[str, str] = settings.FILE_SEPARATORS
        self._encodings: Tuple[str, ...] = settings.FILE_ENCODINGS
        self._header: str = settings.FILE_HEADER
        self._data: Optional[DataFrame] = None
        self._data_path: str = settings.DATA_RESOURCE
        self._file_name: Optional[str] = None

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if type(value) is str:
            self._file_name = value

        else:
            raise ValueError('The param "file_name" must be a string')

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, value):
        if isinstance(value, str):
            self._data_path = value

        else:
            raise ValueError("Try to set data path with a no 'str' value.")

    def load_csv_using_conf(
        self,
        file_name: str,
        separator: str,
        encoding: str,
        header: Optional[str] = None,
    ) -> Optional["DataFrame"]:
        """Read a csv file.

        This method read a csv using a specific configuration provided by the user.

        Args:
            file_name: The name of the file.
            separator: the separator used in the file.
            encoding: encoding type used to successfully read text in the file.

        Returns:
            A DataFrame if the combination of parameters allow to perform the
            read operation. None otherwise.
        """

        self._file_name = file_name
        path_file = self._data_path + self._file_name

        file_header = header if header else settings.FILE_HEADER

        try:
            self._data = pd.read_csv(
                path_file, sep=separator, encoding=encoding, header=file_header
            )

        except Exception as e:
            logger.error(
                "Error while reading csv file using the following parameters: '%s'", e
            )
            logger.error(
                f"    Separator: {separator} - Encoding: {encoding} - Header: {file_header}"
            )

            return

        return self._data

    def load_csv_file(self, *, file_name: str) -> "DataFrame":
        """Read a csv file.

        This method read a csv file by trying to infer its right configuration
        of parameters: separator, encoding and header.

        Args:
            file_name: The name of the file.

        Returns:
            A DataFrame if the right combination of parameters is found. None otherwise.
        """
        self._file_name = file_name
        path_file = self._data_path + self._file_name

        for separator in self._separators.values():
            if not self._data:
                for encoding in self._encodings:
                    try:
                        logger.info("Reading file: '%s'", path_file)
                        logger.info("    Using file separator: '%s'", separator)
                        logger.info("    Using file encoding: '%s'", encoding)
                        self._data = pd.read_csv(
                            path_file,
                            sep=separator,
                            header=self._header,
                            encoding=encoding,
                        )

                        logger.info("File successfully loaded.")

                        break
                    except pd.errors.ParserError as e:
                        logger.error("    ParserError error while reading: '%s'", e)
                        logger.error(f"    Bad separator: '%s'", separator)
                        break

                    except UnicodeDecodeError as e:
                        logger.error(
                            "    UnicodeDecodeError error while reading: '%s'", e
                        )
                        logger.error("    Bad encoding: '%s' - '%s'", encoding, e)
                        continue

                    except Exception as e:
                        logger.error(
                            "    Unhandled error while reading the file: '%s'", e
                        )
                        logger.error("    Error type: '%s'", type(e))

        return self._data

    def __str__(self):
        return f"Filename: {self._file_name} - Path: {self._data_path}"
