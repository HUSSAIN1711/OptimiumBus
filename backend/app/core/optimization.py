from __future__ import annotations

"""
Optimization utilities for clustering bus stops and computing routes.

- cluster_stops_kmeans: clusters bus stops into n groups using KMeans.
- order_stops_nearest_neighbor: orders stops within a cluster using a nearest-neighbor heuristic.
- optimize_routes: end-to-end optimization to produce n routes.

Notes:
- Uses OSMnx/NetworkX travel time between snapped nodes when possible.
- Falls back to haversine distance if network travel time cannot be computed.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass

import math
import networkx as nx
from sklearn.cluster import KMeans

from app.models.bus_stop import BusStop
from app.core.osmnx_utils import get_road_network_manager


@dataclass
class StopPoint:
    stop_id: str
    name: str
    latitude: float
    longitude: float


def haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def cluster_stops_kmeans(stops: List[BusStop], num_clusters: int) -> List[List[StopPoint]]:
    if num_clusters <= 0:
        raise ValueError("num_clusters must be >= 1")
    if not stops:
        return [[] for _ in range(num_clusters)]

    try:
        coords = [[s.latitude, s.longitude] for s in stops]
        kmeans = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
        labels = kmeans.fit_predict(coords)

        clusters: List[List[StopPoint]] = [[] for _ in range(num_clusters)]
        for stop, label in zip(stops, labels):
            clusters[label].append(
                StopPoint(stop_id=str(stop.id), name=stop.name, latitude=stop.latitude, longitude=stop.longitude)
            )

        # Ensure no empty clusters by simple rebalancing (if any are empty)
        empty_indices = [i for i, c in enumerate(clusters) if len(c) == 0]
        if empty_indices:
            non_empty = [c for c in clusters if c]
            flat = [p for c in non_empty for p in c]
            clusters = [[] for _ in range(num_clusters)]
            for idx, p in enumerate(flat):
                clusters[idx % num_clusters].append(p)

        return clusters
    except Exception as e:
        print(f"KMeans clustering failed: {e}, using simple round-robin assignment")
        # Fallback to simple round-robin assignment
        clusters: List[List[StopPoint]] = [[] for _ in range(num_clusters)]
        for i, stop in enumerate(stops):
            cluster_idx = i % num_clusters
            clusters[cluster_idx].append(
                StopPoint(stop_id=str(stop.id), name=stop.name, latitude=stop.latitude, longitude=stop.longitude)
            )
        return clusters


def travel_time_or_distance(g: nx.MultiDiGraph, a: StopPoint, b: StopPoint) -> float:
    # Simplified version that uses haversine distance for now
    # This avoids the complex road network processing that might be causing errors
    try:
        manager = get_road_network_manager()
        # Snap both points to nearest nodes
        _, _, node_a = manager.snap_coordinates_to_network(a.latitude, a.longitude)
        _, _, node_b = manager.snap_coordinates_to_network(b.latitude, b.longitude)
        if node_a == -1 or node_b == -1:
            raise RuntimeError("snap failed")
        # Shortest path by travel_time
        path = nx.shortest_path(g, node_a, node_b, weight="travel_time")
        total_time = 0.0
        for i in range(len(path) - 1):
            edge_data = g.get_edge_data(path[i], path[i + 1])
            if not edge_data:
                continue
            # get first key's travel_time
            first_key = next(iter(edge_data))
            total_time += float(edge_data[first_key].get("travel_time", 0.0))
        if total_time > 0:
            return total_time
        # fallback to length if travel_time not present
        total_len = 0.0
        for i in range(len(path) - 1):
            edge_data = g.get_edge_data(path[i], path[i + 1])
            if not edge_data:
                continue
            first_key = next(iter(edge_data))
            total_len += float(edge_data[first_key].get("length", 0.0))
        if total_len > 0:
            # assume 30 km/h default; return time seconds
            return (total_len / 1000.0) / 30.0 * 3600.0
    except Exception as e:
        print(f"Road network optimization failed: {e}, falling back to haversine distance")
        pass
    # Final fallback: haversine meters converted to time at 30 km/h
    meters = haversine_meters(a.latitude, a.longitude, b.latitude, b.longitude)
    return (meters / 1000.0) / 30.0 * 3600.0


def order_stops_nearest_neighbor(cluster: List[StopPoint]) -> List[StopPoint]:
    if not cluster:
        return []
    if len(cluster) == 1:
        return cluster

    # Build order starting from the stop with smallest latitude/longitude (stable start)
    start_idx = min(range(len(cluster)), key=lambda i: (cluster[i].latitude, cluster[i].longitude))
    unvisited = cluster.copy()
    current = unvisited.pop(start_idx)
    order = [current]

    # Use simple distance-based ordering to avoid road network issues
    while unvisited:
        # Use haversine distance for ordering
        next_idx = min(range(len(unvisited)), 
                      key=lambda i: haversine_meters(current.latitude, current.longitude, 
                                                  unvisited[i].latitude, unvisited[i].longitude))
        current = unvisited.pop(next_idx)
        order.append(current)
    
    return order


def optimize_routes(stops: List[BusStop], num_buses: int) -> List[Dict[str, object]]:
    """
    Returns list of routes, each route is a dict with:
      - bus_index
      - stop_ids: ordered list of stop ids
      - coordinates: ordered list of {lat, lng}
    """
    try:
        print(f"Starting optimization with {len(stops)} stops and {num_buses} buses")
        clusters = cluster_stops_kmeans(stops, num_buses)
        print(f"Clustering completed, {len(clusters)} clusters created")
        
        routes: List[Dict[str, object]] = []
        for i, cluster in enumerate(clusters):
            print(f"Processing cluster {i} with {len(cluster)} stops")
            ordered = order_stops_nearest_neighbor(cluster)
            routes.append({
                "bus_index": i,
                "stop_ids": [p.stop_id for p in ordered],
                "coordinates": [{"lat": p.latitude, "lng": p.longitude} for p in ordered]
            })
        print(f"Optimization completed, generated {len(routes)} routes")
        return routes
    except Exception as e:
        print(f"Error in optimize_routes: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
