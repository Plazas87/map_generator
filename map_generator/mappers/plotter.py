import logging
from typing import Tuple, List, Optional

from folium.plugins import MeasureControl, HeatMap
from folium import (
    Map,
    GeoJson,
    Popup,
    Marker,
    Tooltip,
    CustomIcon,
    CircleMarker,
    LayerControl,
)

import settings

logger = logging.getLogger(__name__)


class MapBuilder:
    """MapBuilder class."""

    def __init__(
        self,
        location: Tuple[float, float] = settings.DEFAULT_INITIAL_LOCATION,
        map_zoom: int = settings.DEFAULT_ZOOM,
        output_path: str = settings.DEFAULT_OUTPUT_PATH,
    ) -> None:
        self._map: "Map"
        self._map_zoom = map_zoom
        self._location = location
        self._output_path = output_path

    @property
    def location(self):
        """Return the location."""
        return self._location

    @location.setter
    def location(self, value: Tuple[float, float]) -> None:
        """Set the location."""
        if (
            len(value) == 2
            and isinstance(value[0], float)
            and isinstance(value[1], float)
        ):
            self._location = value

    @property
    def _map_zoom(self):
        """Get the zoom of the map."""
        return self._zoom

    @_map_zoom.setter
    def _map_zoom(self, value):
        """Set the initial zoom of the map."""
        if 1 <= value < 17 and isinstance(value, int):
            self._zoom = value
        else:
            raise ValueError("Please use a zoom value between 1 - 16")

    @property
    def map(self) -> "Map":
        """Return a folium Map instance."""
        return self._map

    @map.setter
    def map(self, value) -> None:
        if isinstance(value, Map):
            self._map = value

        else:
            logger.error("The value must be an folium.Map instance")
            raise ValueError("The value must be an folium.Map instance")

    def _create_popup(self, text: str, max_with: int = 900) -> "Popup":
        popup = Popup(text, max_width=max_with)
        logger.debug("Complete")

        return popup

    def _create_custom_icon(
        self, icon_file_name: str, icon_size: Optional[Tuple[int, int]]
    ):
        size = settings.DEFAULT_CUSTOM_ICON_SIZE

        if icon_size:
            size = icon_size

        custom_icon = CustomIcon(
            icon_image=settings.DEFAULT_CUSTOM_ICONS_PATH + icon_file_name,
            icon_size=size,
        )
        logger.debug("Complete")

        return custom_icon

    def _create_tooltip(self, tooltip_text) -> "Tooltip":
        tooltip = Tooltip(tooltip_text)
        logger.debug("Complete")

        return tooltip

    def initialize_map(self) -> "MapBuilder":
        """Initializes an empty map using an initial location"""
        self._map = Map(
            location=self.location, tiles="OpenStreetMap", zoom_start=self._map_zoom
        )

        return self

    def add_polygon(
        self,
        polygon_corrdinates,
        popup_text: Optional[str] = None,
        popup_maxwith: Optional[int] = None,
    ) -> "MapBuilder":
        """Add a polygon to an existing map."""
        polygon = settings.DEFAULT_POLYGON_COORDINATES

        if polygon_corrdinates:
            polygon = polygon_corrdinates

        gj = GeoJson(
            data={
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": polygon},
            },
            name="Madrid Central",
        )

        if popup_text:
            popup = self._create_popup(text=popup_text, max_with=popup_maxwith)
            gj.add_child(popup)

        gj.add_to(self._map)

        return self

    def add_marker(
        self,
        *,
        location: Tuple[int, int],
        legend: Optional[str] = None,
        tooltip_text: Optional[str] = None,
        icon_file_name: Optional[str] = None,
        icon_size: Optional[Tuple[int, int]] = None,
    ) -> "MapBuilder":
        """Add a marker to and existing map.

        Args:
            location: A locations in the format (lat, lon).
            legend: Message to be shown when the marker is clicked.
            tooltip_text: Message to be shown when the mouse pass over the marker.
            icon_file_name: file name of the custom icon to use, for example: 'cus_icon.png'.
            icon_size: Size of the icon to show.

        Returns:
            Map instance
        """

        try:
            # Create a Standard Marker with a name to render
            logger.debug("Creating the marker...")
            marker = Marker(location=location, popup=legend)

            # If there is a custom icon, add it to the market
            if icon_file_name is not None:
                logger.debug("Adding a custom icon to the marker...")
                icon = self._create_custom_icon(
                    icon_file_name=icon_file_name, icon_size=icon_size
                )
                marker.add_child(icon)

            # If a tooltip is passed then add it to the marker
            if tooltip_text is not None:
                logger.debug("Adding a tooltip to the marker...")
                tooltip = self._create_tooltip(tooltip_text=tooltip_text)
                marker.add_child(tooltip)

            marker.add_to(self._map)

        except TypeError:
            logger.error("Location must be a tuple as follows: (lat, lon)")

        except FileNotFoundError as e:
            logger.error("FileNotFoundError: %s", e)

        except Exception as e:
            logger.error("Unknown error while creating the marker: %s", e)

        return self

    def add_layer_control(self) -> "MapBuilder":
        """Add a LayerControl to the map."""
        layer_control = LayerControl().add_to(self._map)
        layer_control.add_to(self._map)
        return self

    def add_measure_control(self) -> "MapBuilder":
        """Add MeasureControl to the map."""
        measure_control = MeasureControl()
        self._map.add_child(measure_control)

        return self

    def add_traffic_station_marker(
        self,
        locations: List[Tuple[float, float]],
        station_names: List[List[int]] = None,
        legend: Optional[str] = None,
    ) -> None:
        """
        Create circle marker for each location.

        Args:
            locations: A list containing coordinates as list pairs [[lat1, lon1], ...]
            station_names: Name to be rendered for each location.
            legend: pending

        Returns:
            None
        """

        if station_names is None:
            station_names = ([i] for i in range(len(locations)))

        for location, stat_name in zip(locations, station_names):
            try:
                tooltip_instance = Tooltip(
                    f"Station: {stat_name[0]}"
                    f"<br>Lat: {round(location[0], 4)}"
                    f"<br>Lon: {round(location[1], 4)}"
                )

                CircleMarker(
                    location=tuple(location),
                    tooltip=tooltip_instance,
                    popup=legend,
                    radius=2,
                    color="red",
                ).add_to(self._map)

            except TypeError:
                logger.error("Location must be a tuple (lat, lon)")
                logger.info("Location skipped. Continue with the next one.")
                continue

            except FileNotFoundError:
                logger.error("FileNotFoundError: can't find the icon.")
                break

            except Exception as e:
                logger.error("Unknown error while creating the circle marker: %s", e)
                logger.info("Location skipped. Continue with the next one.")
                continue

    # agregar esta función comopleta al proyecto
    def add_traffic_heatmap(self, locations):
        """Generates a HeatMap using a bunch of traffic station points"""
        heat_map = HeatMap(
            locations,
            name="Tráfico",
            radius=14,
            min_opacity=0.8,
            gradient={0.4: "blue", 0.8: "lime", 1: "red"},
        )
        heat_map.add_to(self._map)

    def save_map(self, file_name) -> None:
        """Save the map as .hmtl using a given name"""
        # Build the map's output path
        output_filename = self._output_path + file_name + ".html"

        logger.info("Saving the map...")
        self._map.save(output_filename)
        logger.info("Saved in: %s.", output_filename)


if __name__ == "__main__":
    madrid_map = MapBuilder()
    madrid_map.save_map("test")
