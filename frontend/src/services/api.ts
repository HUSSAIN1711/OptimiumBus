import axios from 'axios';
import { BusStop, OptimizationResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const busStopAPI = {
  // Get all bus stops
  getAll: async (): Promise<BusStop[]> => {
    const response = await api.get('/stops/');
    return response.data.stops;
  },

  // Create a new bus stop
  create: async (busStop: Omit<BusStop, 'id' | 'created_at' | 'updated_at'>): Promise<BusStop> => {
    const response = await api.post('/stops/', busStop);
    return response.data;
  },

  // Update a bus stop
  update: async (id: string, updates: Partial<BusStop>): Promise<BusStop> => {
    const response = await api.put(`/stops/${id}`, updates);
    return response.data;
  },

  // Delete a bus stop
  delete: async (id: string): Promise<void> => {
    await api.delete(`/stops/${id}`);
  },

  // Get nearby bus stops
  getNearby: async (lat: number, lng: number, radiusKm: number = 1.0): Promise<BusStop[]> => {
    const response = await api.get('/stops/nearby/', {
      params: { latitude: lat, longitude: lng, radius_km: radiusKm }
    });
    return response.data;
  },
};

export const optimizationAPI = {
  // Optimize routes
  optimizeRoutes: async (numBuses: number): Promise<OptimizationResponse> => {
    const response = await api.post('/optimize/routes', null, {
      params: { num_buses: numBuses }
    });
    return response.data;
  },
};
