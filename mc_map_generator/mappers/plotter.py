#!usr/bin/env python
import logging
from typing import Tuple, List, Optional

import pandas as pd
import vincent
from folium.plugins import MeasureControl, HeatMap, TimestampedGeoJson
from folium import Map, GeoJson, Popup, Marker, Tooltip, CustomIcon, CircleMarker, Vega, LayerControl


logger = logging.getLogger(__name__)


class Plotter:
    """Plotter class."""
    MADRID_LOCATION = (40.4167598, -3.7040395)
    INITIAL_ZOOM = 13

    def __init__(
            self,
            location: Tuple[float, float] = MADRID_LOCATION,
            zoom: int = INITIAL_ZOOM
    ) -> None:
        self.zoom = zoom
        self._location = location
        self.map = self._initialize_map()
        self._maps_path = './mc_map_generator/resources/images/maps/'

    @property
    def location(self):
        """Return the location."""
        return self._location

    @location.setter
    def location(self, value: Tuple[float, float]) -> None:
        """Set the location."""
        if len(value) == 2 and isinstance(value[0], float) and isinstance(value[1], float):
            self._location = value

    @property
    def zoom(self):
        """Get the initial zoom of the map."""
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        """Set the initial zoom of the map."""
        if 1 < value < 17:
            self._zoom = value
        else:
            raise ValueError('Please use a zoom value between 1 - 16')

    @property
    def map(self) -> "Map":
        """Return a folium Map instance."""
        return self._map

    @map.setter
    def map(self, value) -> None:
        if isinstance(value, Map):
            self._map = value

        else:
            raise ValueError('The value must be an d instance of the class folium.Map()')

    def _initialize_map(self) -> "Map":
        """Initializes an empty map with Madrid Central's regions on it"""
        m = Map(
            location=self.location,
            tiles='OpenStreetMap',
            zoom_start=self.zoom
        )

        gj = GeoJson(data={
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
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
                    [-3.714029, 40.410539]
                ]]
            }
        }, name="Madrid Central")

        gj.add_child(Popup('Área de Madrid Central', max_width=900))  # agregar al proyecto
        gj.add_to(m)
        return m

    def add_station_marker(self, locations, station_names=None, legend=None, **kwargs):
        """Add air stations to the map. Add as many as the the lenght of the locatios parameter"""
        if station_names is None:
            station_names = [[i] for i in range(len(locations))]

        for location, stat_name in zip(locations, station_names):
            try:
                Marker(location=location,
                              tooltip=Tooltip(
                                  f'Estación: {stat_name[0]}<br>Latitud: {round(location[0], 4)}<br>Longitud: {round(location[1], 4)}'),
                              popup=legend,
                              icon=CustomIcon(icon_image='./mc_map_generator/resources/images/icons/forecast.png',
                                                     icon_size=(40, 40))).add_to(self._map)
            except TypeError as e:
                print("El parametro location debe ser un de la forma [lat, lon] ó (lat,lon)")
                print('Probando con la siguiente estación...')
                continue

            except FileNotFoundError as e:
                print('El archivo para representar las estaciones no se encuentra en la carpeta "icons"')
                break

            except Exception as e:
                print(e)

    def add_traffic_station_marker(
        self,
        locations: List[List[float, float]],
        station_names: List[List[int]] = None,
        legend: Optional[str] = None
    ) -> None:
        """
        Create circle marker for each location.

        Args:
            locations: A list containing coordinates as list pairs [[lat1, lon1], [lat2, lon2], ...]
            station_names: Name to be rendered for each location. Must be the same size as locations
            legend: pending

        Returns:
            None
        """

        if station_names is None:
            station_names = ([i] for i in range(len(locations)))

        for location, stat_name in zip(locations, station_names):
            try:
                tooltip_instance = Tooltip(
                    f'Station: {stat_name[0]}<br>Lat: {round(location[0], 4)}<br>Lon: {round(location[1], 4)}'
                )

                CircleMarker(
                    location=tuple(location),
                    tooltip=tooltip_instance,
                    popup=legend,
                    radius=2,
                    color='red'
                ).add_to(self._map)

            except TypeError as e:
                logger.error("Location must be a tuple (lat, lon)")
                logger.info("Location skipped. Continue with the next one.")
                continue

            except Exception as e:
                logger.error("Unknown error while creating the circle marker")
                logger.info("Location skipped. Continue with the next one.")
                continue

    def add_air_station_marker_with_graph(self, data, *args, **kwargs):
        """Esta función se encarga de agregar graficos a los marcadores existentes"""
        locations = data.iloc[:, [1, 2]]
        station_names = data.iloc[:, [3]]

        station_ids = list(pd.unique(data.id))
        station_groups = data.groupby('id')

        for station_id in station_ids:
            filtered_data = station_groups.get_group(station_id)
            print('***** data get group')
            print(type(filtered_data))
            print(filtered_data.head())
            plot_data = filtered_data.groupby(['magnitude', 'year', 'month', 'day']).agg(
                {'value': 'mean'}).reset_index()
            print('***** data plot data')
            print(type(plot_data))
            print(plot_data.head())

            x = [int(hour) for hour in list(plot_data['day'])]
            y = [int(value) for value in list(plot_data['value'])]
            print(x)
            print(y)

            xy_values = {
                'x': x,
                'y': y,
            }
            scatter_chart = vincent.Scatter(xy_values,
                                            iter_idx='x',
                                            width=600,
                                            height=300)

            scatter_chart.axis_titles(x='Día', y='Promedio Dióxido de Nitrogeno día')

            popup_scatter_plot = Popup(max_width=900).add_child(
                Vega(scatter_chart, height=350, width=700))

            air_quality_station = [filtered_data.iloc[0, 1], filtered_data.iloc[0, 2]]
            print(air_quality_station)
            station_name = [filtered_data.iloc[0, 3]]
            print(station_name)
            Marker(location=air_quality_station,
                          tooltip=Tooltip(
                              f'Estación: {station_name[0]}<br>Latitud: {round(air_quality_station[0], 4)}<br>Longitud: {round(air_quality_station[1], 4)}'),
                          popup=popup_scatter_plot,
                          icon=CustomIcon(icon_image='icons/forecast.png',
                                                 icon_size=(40, 40))).add_to(self._map)

    # agregar esta función comopleta al proyecto
    def add_traffic_heatmap(self, locations):
        """Generates a HeatMap using a bunch of traffic station points"""
        heat_map = HeatMap(locations, name='Tráfico', radius=14, min_opacity=0.8,
                           gradient={0.4: 'blue', 0.8: 'lime', 1: 'red'})
        heat_map.add_to(self._map)

    def add_traffic_timestamped_map(self, gjson_timestamped):
        TimestampedGeoJson(
            {'type': 'FeatureCollection',
             'features': gjson_timestamped},
            period='PT1H',
            add_last_point=True,
            auto_play=False,
            loop=False, max_speed=1,
            loop_button=True,
            date_options='YYYY/MM/DD HH',
            time_slider_drag_update=True).add_to(self._map)

    def add_market_with_shape_color(self, locations, station_names=None, shapes=None, colors=None, legends=None,
                                    **kwargs):
        """Agrega al mapa el tantas estaciones de calidad del aire como ubicaciones existan dentro del parametro
        locations"""
        if station_names is None:
            station_names = [[i] for i in range(len(locations))]

        if shapes is None:
            shapes = [[2] for i in range(len(locations))]

        if colors is None:
            colors = [['red'] for i in range(len(locations))]

        for location, stat_name, shape, color, legend in zip(locations, station_names, shapes, colors, legends):
            try:
                CircleMarker(location=location,
                                    tooltip=Tooltip(
                                        f'Estación: {stat_name[0]}<br>Latitud: {round(location[0], 4)}<br>Longitud: {round(location[1], 4)}<br>\
                                            Correlación: {legend[0]}'),
                                    popup=legend,
                                    radius=shape[0] * 75,
                                    fill=True,
                                    fill_color=color[0],
                                    fill_opacity=0.7,
                                    color='black').add_to(self._map)

            except TypeError as e:
                print("El parametro location debe ser un de la forma [lat, lon] ó (lat,lon)")
                print('Probando con la siguiente estación...')
                continue

            except FileNotFoundError as e:
                print('El archivo para representar las estaciones no se encuentra en la carpeta "icons"')
                break

            except Exception as e:
                print(e)

    @staticmethod
    def create_json(data):
        features = []
        for _, row in data.iterrows():
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [row['longitude'], row['latitude']]
                },
                'properties': {
                    'time': row['step'].__str__(),
                    'style': {'color': row['color']},
                    'icon': 'circle',
                    'iconstyle': {
                        'fillOpacity': 0.9,
                        'radius': 5
                    }
                }
            }
            features.append(feature)
        return features

    @staticmethod
    def color_coding(row, max_value, min_value):
        interval_lenght = max_value - min_value
        interval_size = interval_lenght / 10

        if min_value <= row['value'] < (min_value + interval_size * 1):
            return '#00ffea'

        elif (min_value + interval_size * 1) <= row['value'] < (min_value + interval_size * 2):
            return '#00ff88'

        elif (min_value + interval_size * 2) <= row['value'] < (min_value + interval_size * 3):
            return '#0dff00'

        elif (min_value + interval_size * 3) <= row['value'] < (min_value + interval_size * 4):
            return '#91ff00'

        elif (min_value + interval_size * 4) <= row['value'] < (min_value + interval_size * 5):
            return '#f2ff00'

        elif (min_value + interval_size * 5) <= row['value'] < (min_value + interval_size * 6):
            return '#ffcc00'

        elif (min_value + interval_size * 6) <= row['value'] < (min_value + interval_size * 7):
            return '#ff7b00'

        elif (min_value + interval_size * 7) <= row['value'] < (min_value + interval_size * 8):
            return '#ff5500'

        elif (min_value + interval_size * 8) <= row['value'] < (min_value + interval_size * 9):
            return '#ff7f00'

        elif (min_value + interval_size * 9) <= row['value'] <= (min_value + interval_size * 10):
            return '#ff0000'

    def generate_map(self, file_name):
        """Generates a .hmtl map using a given name"""
        LayerControl().add_to(self._map)
        self._map.add_child(MeasureControl())
        self.map.save(self._maps_path + file_name + '.html')


if __name__ == "__main__":
    madrid_map = Plotter()
    madrid_map.generate_map("test")
