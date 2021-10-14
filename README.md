## Map generator
This project is a tool to easily create maps from '.csv' files that contain coordinates
(latitude and longitude). It is basically a wrapper over some methods of the 'folium'
Python package to hide some complexity from the final user.

### Requirements

Python 3.8+

### Before running
As I already mention, this is a wrapper over some common and useful methods of
the Folium Python package. Said that, this project contains some basic examples
of maps that you can create using some data and a few lines of code. If you need
to generate more complex visualizations I highly recommend you to modify the
'__main__.py' file to write you own 'Typer' commands.

Before using the tool for the first time you must:

1. Clone the project
2. Crate a new virtual environment for the project.
3. Install dependencies: `pip install -r requirements.txt`

Now, you need a valid '.csv' file that contains at least two columns to specify
the coordinates of each location you are about to plot: 'latitude' and 'longitude'.
You can name these columns as you want. The only important information that you need
to be aware of is:
1. The '.csv' file must be located at: `./resources/data/<your_csv_file_name>`
2. The length of these columns must be equal.
3. Values within these columns must be a float value, for example: 3.21352154.
Please note that the number of decimals is related to the location's precision.
4. The indexes of these columns. Suppose that you have a '.csv' with the
following columns:
`CODIGO;ESTACION;...;LONGITUD;LATITUD`
Please take note of the indexes of 'latitude' and 'longitude' columns. You will
need it later to generate a map.

### Quick start
To generate your first map, the project contains an example '.cvs' file located at
`./resources/data/madrid_air_quality_stations.csv`. This file was downloaded from
[Portal de datos abiertos del Ayuntamiento de Madrid - Datos meteorológicos. Estaciones de control](https://datos.madrid.es/sites/v/index.jsp?vgnextoid=2ac5be53b4d2b610VgnVCM2000001f4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD).
This file contains information related to the location of the existing air quality stations in Madrid, Spain. As we want to visualize these stations in a Map, we are going to focus in the columns
'**latitude**' and '**longitude**'. The first one is located at index 24 and the latter
id located at index 25.

Now, we are ready to generate our first map. As we only care about coordinates for this Map,
a default Marker and name will be used to show locations. You can customize some aspects of your
Map by selecting other columns of your '.csv' file like the Marker's name, icon, legend and
tooltip. You can even include nested graphs to you Market (coming soon).

Before generating your first Map you need to be familiar with the notation used to indicate
columns in your '.csv':

- `[LATITUDE,LONGITUDE,LEGEND,TOOLTIP]`

As you can see, it is possible to define up to four positions in our '.csv' file. The columns
'latitude' and 'longitude' are always required. The other ones are optional.

In this case, to indicate the 'latitude' and 'longitude' of our '.csv' you must use
the following notation:

- `[25,24]`

Finally, to generate a Map run:

```python map_generator [25,24]```

This command generates a Map using the information from the '.csv' file and save the result in
the folder `./generated_maps/` so, cd to this folder and open your Map using a browser.
