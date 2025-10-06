import React, { useState } from 'react';
import { BusStop } from '../types';

interface BusStopFormProps {
  onSubmit: (busStop: Omit<BusStop, 'id' | 'created_at' | 'updated_at'>) => void;
  onCancel: () => void;
  initialData?: Partial<BusStop>;
}

const BusStopForm: React.FC<BusStopFormProps> = ({ onSubmit, onCancel, initialData }) => {
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    description: initialData?.description || '',
    latitude: initialData?.latitude || 0,
    longitude: initialData?.longitude || 0,
    demand_weight: initialData?.demand_weight || 0.5,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'latitude' || name === 'longitude' || name === 'demand_weight' 
        ? parseFloat(value) || 0 
        : value
    }));
  };

  return (
    <div className="bus-stop-form">
      <h3>{initialData ? 'Edit Bus Stop' : 'Add New Bus Stop'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Enter bus stop name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Enter description (optional)"
            rows={3}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="latitude">Latitude *</label>
            <input
              type="number"
              id="latitude"
              name="latitude"
              value={formData.latitude}
              onChange={handleChange}
              required
              step="any"
              placeholder="e.g., 33.6846"
            />
          </div>

          <div className="form-group">
            <label htmlFor="longitude">Longitude *</label>
            <input
              type="number"
              id="longitude"
              name="longitude"
              value={formData.longitude}
              onChange={handleChange}
              required
              step="any"
              placeholder="e.g., -117.8265"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="demand_weight">Demand Weight (0.0 - 1.0)</label>
          <input
            type="number"
            id="demand_weight"
            name="demand_weight"
            value={formData.demand_weight}
            onChange={handleChange}
            min="0"
            max="1"
            step="0.1"
            placeholder="0.5"
          />
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} className="btn-secondary">
            Cancel
          </button>
          <button type="submit" className="btn-primary">
            {initialData ? 'Update' : 'Create'} Bus Stop
          </button>
        </div>
      </form>
    </div>
  );
};

export default BusStopForm;
