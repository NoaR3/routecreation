import math
from math import radians, sin, cos, sqrt, atan2
from node import Node
from way import Way


class Edge:
    def __init__(self, source, target, weight, tags):
        self.source = source
        self.target = target
        self.weight = weight
        self.length = euclidean_distance(source, target)
        self.tags = tags


def euclidean_distance(coord1, coord2):

    lat1, lon1 = coord1.latitude, coord1.longitude
    lat2, lon2 = coord2.latitude, coord2.longitude

    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * math.cos(math.radians(lat1))

    delta_lat_km = (lat2 - lat1) * km_per_deg_lat
    delta_lon_km = (lon2 - lon1) * km_per_deg_lon

    distance = math.sqrt(delta_lat_km ** 2 + delta_lon_km ** 2)

    return distance


