"""
OSMnx utility functions for road network integration

This module provides functions to download, cache, and work with OpenStreetMap
road network data using OSMnx. It handles downloading road graphs for specific
areas and provides coordinate snapping functionality.
"""

import os
import pickle
from typing import Tuple, Optional, Dict, Any
import osmnx as ox
import networkx as nx
import numpy as np
from geopy.distance import geodesic
import logging

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache directory for storing downloaded road networks
CACHE_DIR = "road_networks"
os.makedirs(CACHE_DIR, exist_ok=True)


class RoadNetworkManager:
    """
    Manages road network data using OSMnx
    
    This class handles downloading, caching, and working with OpenStreetMap
    road network data for a specific geographic area.
    """
    
    def __init__(self, place_name: str = "Irvine, California, USA"):
        """
        Initialize the road network manager
        
        Args:
            place_name: Name of the place to download road network for
        """
        self.place_name = place_name
        self.graph = None
        self.cache_file = os.path.join(CACHE_DIR, f"{place_name.replace(', ', '_').replace(' ', '_')}.pkl")
        
    def get_road_network(self, force_download: bool = False) -> nx.MultiDiGraph:
        """
        Get the road network graph, downloading if necessary
        
        Args:
            force_download: Force re-download even if cached version exists
            
        Returns:
            nx.MultiDiGraph: Road network graph
        """
        # Try to load from cache first
        if not force_download and os.path.exists(self.cache_file):
            try:
                logger.info(f"Loading road network from cache: {self.cache_file}")
                with open(self.cache_file, 'rb') as f:
                    self.graph = pickle.load(f)
                logger.info(f"Loaded road network with {len(self.graph.nodes)} nodes and {len(self.graph.edges)} edges")
                return self.graph
            except Exception as e:
                logger.warning(f"Failed to load from cache: {e}. Will download fresh data.")
        
        # Download fresh data
        logger.info(f"Downloading road network for: {self.place_name}")
        try:
            # Download road network
            self.graph = ox.graph_from_place(
                self.place_name,
                network_type='drive',  # Include all driveable roads
                simplify=True  # Simplify the graph topology
            )
            
            # Add edge speeds and travel times
            self.graph = ox.add_edge_speeds(self.graph)
            self.graph = ox.add_edge_travel_times(self.graph)
            
            # Project to UTM for accurate distance calculations
            self.graph = ox.project_graph(self.graph)
            
            logger.info(f"Downloaded road network with {len(self.graph.nodes)} nodes and {len(self.graph.edges)} edges")
            
            # Cache the graph
            self._cache_graph()
            
            return self.graph
            
        except Exception as e:
            logger.error(f"Failed to download road network: {e}")
            raise
    
    def _cache_graph(self):
        """Cache the graph to disk"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.graph, f)
            logger.info(f"Cached road network to: {self.cache_file}")
        except Exception as e:
            logger.warning(f"Failed to cache graph: {e}")
    
    def snap_coordinates_to_network(self, latitude: float, longitude: float) -> Tuple[float, float, int]:
        """
        Snap coordinates to the nearest node in the road network
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Tuple[float, float, int]: (snapped_lat, snapped_lng, node_id)
        """
        if self.graph is None:
            self.get_road_network()
        
        try:
            # Project coordinates to UTM
            point_utm = ox.projection.project_point(latitude, longitude, self.graph.graph['crs'])
            
            # Find nearest node
            nearest_node = ox.nearest_nodes(self.graph, point_utm[0], point_utm[1])
            
            # Get node coordinates
            node_data = self.graph.nodes[nearest_node]
            node_lat = node_data['y']
            node_lng = node_data['x']
            
            # Project back to lat/lng
            snapped_lat, snapped_lng = ox.projection.project_point(
                node_lat, node_lng, self.graph.graph['crs'], to_latlong=True
            )
            
            logger.info(f"Snapped ({latitude}, {longitude}) to ({snapped_lat}, {snapped_lng}) at node {nearest_node}")
            
            return snapped_lat, snapped_lng, nearest_node
            
        except Exception as e:
            logger.error(f"Failed to snap coordinates: {e}")
            # Return original coordinates if snapping fails
            return latitude, longitude, -1
    
    def get_shortest_path(self, start_lat: float, start_lng: float, 
                         end_lat: float, end_lng: float) -> Optional[Dict[str, Any]]:
        """
        Calculate shortest path between two coordinates
        
        Args:
            start_lat: Start latitude
            start_lng: Start longitude
            end_lat: End latitude
            end_lng: End longitude
            
        Returns:
            Dict containing path information or None if no path found
        """
        if self.graph is None:
            self.get_road_network()
        
        try:
            # Snap coordinates to network
            start_lat_snapped, start_lng_snapped, start_node = self.snap_coordinates_to_network(start_lat, start_lng)
            end_lat_snapped, end_lng_snapped, end_node = self.snap_coordinates_to_network(end_lat, end_lng)
            
            if start_node == -1 or end_node == -1:
                logger.warning("Could not snap one or both coordinates to network")
                return None
            
            # Calculate shortest path
            try:
                path = nx.shortest_path(self.graph, start_node, end_node, weight='travel_time')
                
                # Calculate path statistics
                path_length = sum(
                    self.graph.edges[path[i], path[i+1], 0].get('length', 0)
                    for i in range(len(path) - 1)
                )
                
                path_travel_time = sum(
                    self.graph.edges[path[i], path[i+1], 0].get('travel_time', 0)
                    for i in range(len(path) - 1)
                )
                
                return {
                    'path': path,
                    'length_meters': path_length,
                    'travel_time_seconds': path_travel_time,
                    'start_coords': (start_lat_snapped, start_lng_snapped),
                    'end_coords': (end_lat_snapped, end_lng_snapped)
                }
                
            except nx.NetworkXNoPath:
                logger.warning(f"No path found between nodes {start_node} and {end_node}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to calculate shortest path: {e}")
            return None
    
    def get_network_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the road network
        
        Returns:
            Dict containing network statistics
        """
        if self.graph is None:
            self.get_road_network()
        
        return {
            'num_nodes': len(self.graph.nodes),
            'num_edges': len(self.graph.edges),
            'place_name': self.place_name,
            'crs': self.graph.graph.get('crs', 'Unknown'),
            'cache_file': self.cache_file
        }


# Global road network manager instance
road_network_manager = RoadNetworkManager()


def get_road_network_manager() -> RoadNetworkManager:
    """
    Get the global road network manager instance
    
    Returns:
        RoadNetworkManager: The road network manager
    """
    return road_network_manager


def snap_coordinates_to_road_network(latitude: float, longitude: float) -> Tuple[float, float, int]:
    """
    Convenience function to snap coordinates to the road network
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Tuple[float, float, int]: (snapped_lat, snapped_lng, node_id)
    """
    return road_network_manager.snap_coordinates_to_network(latitude, longitude)


def get_shortest_path_between_coordinates(start_lat: float, start_lng: float,
                                        end_lat: float, end_lng: float) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get shortest path between coordinates
    
    Args:
        start_lat: Start latitude
        start_lng: Start longitude
        end_lat: End latitude
        end_lng: End longitude
        
    Returns:
        Dict containing path information or None if no path found
    """
    return road_network_manager.get_shortest_path(start_lat, start_lng, end_lat, end_lng)
