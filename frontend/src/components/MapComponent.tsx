import React, { useEffect, useRef, useState } from 'react';
import { setOptions, importLibrary } from '@googlemaps/js-api-loader';
import { BusStop } from '../types';

interface MapComponentProps {
  busStops: BusStop[];
  routes: Array<{ bus_index: number; stop_ids: string[]; coordinates: Array<{ lat: number; lng: number }> }>;
  onMapClick: (lat: number, lng: number) => void;
  onStopClick: (stop: BusStop) => void;
}

const MapComponent: React.FC<MapComponentProps> = ({ 
  busStops, 
  routes, 
  onMapClick, 
  onStopClick 
}) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [markers, setMarkers] = useState<google.maps.Marker[]>([]);
  const [polylines, setPolylines] = useState<google.maps.Polyline[]>([]);

  // Initialize Google Maps
  useEffect(() => {
    const initMap = async () => {
      try {
        // Set the API key and options
        setOptions({
          key: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
        });

        // Import the Maps library
        const { Map } = await importLibrary('maps');
        
        const mapInstance = new Map(mapRef.current!, {
          center: { lat: 33.6846, lng: -117.8265 }, // Irvine, CA
          zoom: 13,
          mapTypeId: 'roadmap',
        });

        // Add click listener for adding stops
        mapInstance.addListener('click', (event: google.maps.MapMouseEvent) => {
          if (event.latLng) {
            onMapClick(event.latLng.lat(), event.latLng.lng());
          }
        });

        setMap(mapInstance);
      } catch (error) {
        console.error('Error loading Google Maps:', error);
      }
    };

    initMap();
  }, [onMapClick]);

  // Update markers when bus stops change
  useEffect(() => {
    if (!map) return;

    const updateMarkers = async () => {
      try {
        // Import Marker library
        const { Marker } = await importLibrary('marker');
        
        // Clear existing markers
        markers.forEach(marker => marker.setMap(null));

        const newMarkers = busStops.map(stop => {
          const marker = new Marker({
            position: { lat: stop.latitude, lng: stop.longitude },
            map: map,
            title: stop.name,
            label: {
              text: stop.name.charAt(0).toUpperCase(),
              color: 'white',
              fontWeight: 'bold'
            }
          });

          marker.addListener('click', () => {
            onStopClick(stop);
          });

          return marker;
        });

        setMarkers(newMarkers);
      } catch (error) {
        console.error('Error creating markers:', error);
      }
    };

    updateMarkers();
  }, [map, busStops, onStopClick, markers]);

  // Update polylines when routes change
  useEffect(() => {
    if (!map) return;

    const updatePolylines = async () => {
      try {
        // Import Polyline library
        const { Polyline } = await importLibrary('maps');
        
        // Clear existing polylines
        polylines.forEach(polyline => polyline.setMap(null));

        const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8'];

        const newPolylines = routes.map((route, index) => {
          if (route.coordinates.length < 2) return null;

          const path = route.coordinates.map(coord => ({
            lat: coord.lat,
            lng: coord.lng
          }));

          const polyline = new Polyline({
            path: path,
            geodesic: true,
            strokeColor: colors[index % colors.length],
            strokeOpacity: 0.8,
            strokeWeight: 4,
            map: map
          });

          return polyline;
        }).filter(Boolean) as google.maps.Polyline[];

        setPolylines(newPolylines);
      } catch (error) {
        console.error('Error creating polylines:', error);
      }
    };

    updatePolylines();
  }, [map, routes, polylines]);

  return (
    <div 
      ref={mapRef} 
      style={{ 
        width: '100%', 
        height: '500px',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }} 
    />
  );
};

export default MapComponent;
