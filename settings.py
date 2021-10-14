# LOGGER
LOGGING_FILE_NAME = "logging.yaml"

# MAPS CONFIG
DEFAULT_INITIAL_LOCATION = (40.4167598, -3.7040395)
DEFAULT_ZOOM = 13
DEFAULT_OUTPUT_PATH = "./generated_maps/"
LATITUDE = "lat"
LONGITUDE = "lon"
LEGEND = "legend"
TOOLTIP = "tooltip"
DEFAULT_COLUMN_DICT_ORDER = {LATITUDE: 0, LONGITUDE: 1, LEGEND: 2, TOOLTIP: 3}

# Coordinates below draw a polygon over Madrid Central area
DEFAULT_POLYGON_COORDINATES = [
    [
        [-3.711305, 40.406807],
        [-3.702612, 40.404997],
        [-3.693235, 40.407742],
        [-3.692248, 40.409000],
        [-3.694617, 40.415505],
        [-3.690392, 40.424887],
        [-3.696207, 40.427856],
        [-3.702162, 40.429122],
        [-3.705810, 40.429681],
        [-3.714018, 40.430404],
        [-3.715059, 40.428918],
        [-3.711797, 40.424377],
        [-3.714372, 40.422988],
        [-3.712870, 40.421534],
        [-3.714029, 40.410539],
    ]
]

# CUSTOM ICONS
DEFAULT_CUSTOM_ICONS_PATH = "./resources/images/icons/"
DEFAULT_ICON_NAME = "forecast.png"
DEFAULT_CUSTOM_ICON_SIZE = (40, 40)

# FILE READER
FILE_SEPARATORS = {"csv": ",", "s-csv": ";"}
FILE_ENCODINGS = ("iso-8859-1", "utf-8", "latin1")
FILE_HEADER = "infer"

# DATA RESOURCES
DATA_RESOURCE = "./resources/data/"
