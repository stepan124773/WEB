from distance import lonlat_distance
from geocoder import get_coordinates


def way(ad1, ad2):
    a, b = get_coordinates(ad1), get_coordinates(ad2)
    return lonlat_distance(a, b) / 1000
