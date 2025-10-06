import React, { useState } from 'react';

interface OptimizationControlsProps {
  onOptimize: (numBuses: number) => void;
  isLoading: boolean;
  numStops: number;
}

const OptimizationControls: React.FC<OptimizationControlsProps> = ({ 
  onOptimize, 
  isLoading, 
  numStops 
}) => {
  const [numBuses, setNumBuses] = useState(2);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (numBuses > 0 && numBuses <= numStops) {
      onOptimize(numBuses);
    }
  };

  return (
    <div className="optimization-controls">
      <h3>Route Optimization</h3>
      <p>Current stops: {numStops}</p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="numBuses">Number of Buses</label>
          <input
            type="number"
            id="numBuses"
            value={numBuses}
            onChange={(e) => setNumBuses(parseInt(e.target.value) || 1)}
            min="1"
            max={numStops}
            required
          />
        </div>

        <button 
          type="submit" 
          disabled={isLoading || numBuses > numStops || numStops === 0}
          className="btn-primary"
        >
          {isLoading ? 'Optimizing...' : 'Optimize Routes'}
        </button>
      </form>

      {numBuses > numStops && (
        <p className="error-message">
          Number of buses cannot exceed number of stops
        </p>
      )}

      {numStops === 0 && (
        <p className="info-message">
          Add some bus stops first to optimize routes
        </p>
      )}
    </div>
  );
};

export default OptimizationControls;
