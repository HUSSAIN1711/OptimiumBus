import React, { useState, useEffect } from 'react';
import './App.css';
import MapComponent from './components/MapComponent';
import BusStopForm from './components/BusStopForm';
import BusStopList from './components/BusStopList';
import OptimizationControls from './components/OptimizationControls';
import { BusStop, Route } from './types';
import { busStopAPI, optimizationAPI } from './services/api';

function App() {
  const [busStops, setBusStops] = useState<BusStop[]>([]);
  const [routes, setRoutes] = useState<Route[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingStop, setEditingStop] = useState<BusStop | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [clickedCoords, setClickedCoords] = useState<{ lat: number; lng: number } | null>(null);

  // Load bus stops on component mount
  useEffect(() => {
    loadBusStops();
  }, []);

  const loadBusStops = async () => {
    try {
      setIsLoading(true);
      const stops = await busStopAPI.getAll();
      setBusStops(stops);
    } catch (error) {
      console.error('Error loading bus stops:', error);
      alert('Failed to load bus stops. Make sure the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleMapClick = (lat: number, lng: number) => {
    setClickedCoords({ lat, lng });
    setEditingStop(null);
    setShowForm(true);
  };

  const handleStopClick = (stop: BusStop) => {
    setEditingStop(stop);
    setClickedCoords(null);
    setShowForm(true);
  };

  const handleFormSubmit = async (formData: Omit<BusStop, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      setIsLoading(true);
      
      if (editingStop) {
        // Update existing stop
        const updatedStop = await busStopAPI.update(editingStop.id, formData);
        setBusStops(prev => prev.map(stop => stop.id === editingStop.id ? updatedStop : stop));
      } else {
        // Create new stop
        const newStop = await busStopAPI.create(formData);
        setBusStops(prev => [...prev, newStop]);
      }
      
      setShowForm(false);
      setEditingStop(null);
      setClickedCoords(null);
    } catch (error) {
      console.error('Error saving bus stop:', error);
      alert('Failed to save bus stop. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingStop(null);
    setClickedCoords(null);
  };

  const handleDeleteStop = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this bus stop?')) {
      return;
    }

    try {
      setIsLoading(true);
      await busStopAPI.delete(id);
      setBusStops(prev => prev.filter(stop => stop.id !== id));
      setRoutes([]); // Clear routes when stops change
    } catch (error) {
      console.error('Error deleting bus stop:', error);
      alert('Failed to delete bus stop. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOptimize = async (numBuses: number) => {
    try {
      setIsLoading(true);
      const result = await optimizationAPI.optimizeRoutes(numBuses);
      setRoutes(result.routes);
    } catch (error) {
      console.error('Error optimizing routes:', error);
      alert('Failed to optimize routes. Make sure you have bus stops and the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚌 OptimumBus Route Optimizer</h1>
        <p>Click on the map to add bus stops, then optimize routes for multiple buses</p>
      </header>

      <main className="App-main">
        <div className="map-container">
          <MapComponent
            busStops={busStops}
            routes={routes}
            onMapClick={handleMapClick}
            onStopClick={handleStopClick}
          />
        </div>

        <div className="controls-container">
          <OptimizationControls
            onOptimize={handleOptimize}
            isLoading={isLoading}
            numStops={busStops.length}
          />

          <BusStopList
            busStops={busStops}
            onEdit={handleStopClick}
            onDelete={handleDeleteStop}
          />
        </div>
      </main>

      {showForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <BusStopForm
              onSubmit={handleFormSubmit}
              onCancel={handleFormCancel}
              initialData={editingStop || (clickedCoords ? {
                latitude: clickedCoords.lat,
                longitude: clickedCoords.lng,
                name: '',
                description: '',
                demand_weight: 0.5
              } : undefined)}
            />
          </div>
        </div>
      )}

      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner">Loading...</div>
        </div>
      )}
    </div>
  );
}

export default App;