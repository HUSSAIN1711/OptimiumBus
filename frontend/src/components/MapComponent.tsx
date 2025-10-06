import React, { useEffect, useRef, useState } from 'react';
import { Loader } from '@googlemaps/js-api-loader';
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
      const loader = new Loader({
        apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
        version: 'weekly',
        libraries: ['places']
      });

      try {
        const google = await loader.load();
        
        const mapInstance = new google.maps.Map(mapRef.current!, {
          center: { lat: 33.6846, lng: -117.8265 }, // Irvine, CA
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
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

    // Clear existing markers
    markers.forEach(marker => marker.setMap(null));

    const newMarkers = busStops.map(stop => {
      const marker = new google.maps.Marker({
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
  }, [map, busStops, onStopClick]);

  // Update polylines when routes change
  useEffect(() => {
    if (!map) return;

    // Clear existing polylines
    polylines.forEach(polyline => polyline.setMap(null));

    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8'];

    const newPolylines = routes.map((route, index) => {
      if (route.coordinates.length < 2) return null;

      const path = route.coordinates.map(coord => ({
        lat: coord.lat,
        lng: coord.lng
      }));

      const polyline = new google.maps.Polyline({
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
  }, [map, routes]);

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
