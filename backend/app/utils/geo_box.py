import math

from app.models import GeoBoxType, GeoPointType


def coords_to_geo_box(geo_point: GeoPointType) -> GeoBoxType:
    """
    Calculate a 1km square geo_box centered on the given latitude and longitude.

    Parameters:
        - geo_point (GeoPointType): the geographic coordinates
            - lat (float): Latitude of the center point.
            - lon (float): Longitude of the center point.

    Returns:
    - dict: A dictionary with the corners of the geo_box.
    """
    lat = geo_point.get("lat", None)
    lon = geo_point.get("lon", None)

    if not lat or not lon:
        raise ValueError("Latitude and Longitude must be provided.")

    km_deg = 111.0  # 1 degree latitude = 111.0km
    lat_offset = (1 / km_deg) / 2
    lon_offset = (1 / (km_deg * math.cos(math.radians(lat)))) / 2

    # Calculate geo_box corners
    return {
        "top_left": {"lat": lat + lat_offset, "lon": lon - lon_offset},
        "bottom_right": {"lat": lat - lat_offset, "lon": lon + lon_offset},
    }
