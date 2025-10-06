export interface BusStop {
  id: string;
  name: string;
  description?: string;
  latitude: number;
  longitude: number;
  demand_weight: number;
  created_at: string;
  updated_at: string;
}

export interface Route {
  bus_index: number;
  stop_ids: string[];
  coordinates: Array<{ lat: number; lng: number }>;
}

export interface OptimizationResponse {
  routes: Route[];
  num_buses: number;
  num_stops: number;
}
