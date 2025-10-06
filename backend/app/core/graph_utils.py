from typing import Hashable
import math
import networkx as nx


def _haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def snap_to_nearest_node(graph: nx.Graph, latitude: float, longitude: float) -> Hashable:
    """
    Return the node id of the nearest node to the given lat/lng using haversine distance.

    The graph's nodes must have either ('y','x') or ('lat','lng') attributes.
    """
    nearest_node = None
    nearest_dist = float("inf")

    for node_id, data in graph.nodes(data=True):
        if "y" in data and "x" in data:
            nlat, nlng = float(data["y"]), float(data["x"])
        elif "lat" in data and "lng" in data:
            nlat, nlng = float(data["lat"]), float(data["lng"])
        else:
            continue
        d = _haversine_meters(latitude, longitude, nlat, nlng)
        if d < nearest_dist:
            nearest_dist = d
            nearest_node = node_id

    if nearest_node is None:
        raise ValueError("Graph has no nodes with coordinate attributes 'y','x' or 'lat','lng'")

    return nearest_node
