import React from 'react';
import { BusStop } from '../types';

interface BusStopListProps {
  busStops: BusStop[];
  onEdit: (stop: BusStop) => void;
  onDelete: (id: string) => void;
}

const BusStopList: React.FC<BusStopListProps> = ({ busStops, onEdit, onDelete }) => {
  if (busStops.length === 0) {
    return (
      <div className="bus-stop-list">
        <h3>Bus Stops</h3>
        <p className="empty-message">No bus stops added yet. Click on the map to add stops.</p>
      </div>
    );
  }

  return (
    <div className="bus-stop-list">
      <h3>Bus Stops ({busStops.length})</h3>
      <div className="stops-container">
        {busStops.map(stop => (
          <div key={stop.id} className="stop-item">
            <div className="stop-info">
              <h4>{stop.name}</h4>
              {stop.description && <p className="stop-description">{stop.description}</p>}
              <p className="stop-coordinates">
                {stop.latitude.toFixed(6)}, {stop.longitude.toFixed(6)}
              </p>
              <p className="stop-demand">Demand: {stop.demand_weight.toFixed(1)}</p>
            </div>
            <div className="stop-actions">
              <button 
                onClick={() => onEdit(stop)}
                className="btn-small btn-secondary"
              >
                Edit
              </button>
              <button 
                onClick={() => onDelete(stop.id)}
                className="btn-small btn-danger"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BusStopList;
