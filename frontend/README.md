# OptimumBus Frontend

React frontend for the OptimumBus Route Optimization application.

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm
- Google Maps API Key
- Backend API running on http://localhost:8000

### Setup

1. **Install dependencies:**
   ```bash
   cd /Users/hmahuvaw/Coding/OptimumBus/OptimiumBus/frontend
   npm install
   ```

2. **Configure Google Maps API:**
   ```bash
   cp env.example .env
   # Edit .env and add your Google Maps API key
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

The app will open at http://localhost:3000

## 🗺️ Features

- **Interactive Map**: Click to add bus stops with coordinate snapping
- **Bus Stop Management**: Create, edit, and delete bus stops
- **Route Optimization**: Optimize routes for multiple buses using clustering
- **Real-time Visualization**: See optimized routes as colored polylines on the map

## 🔧 Configuration

### Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select existing one
3. Enable the Maps JavaScript API
4. Create credentials (API Key)
5. Add the key to your `.env` file:
   ```
   REACT_APP_GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

### Backend Connection

The frontend connects to the backend API at `http://localhost:8000/api/v1`. Make sure the backend is running before starting the frontend.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── MapComponent.tsx      # Google Maps integration
│   │   ├── BusStopForm.tsx       # Add/edit bus stop form
│   │   ├── BusStopList.tsx       # List of bus stops
│   │   └── OptimizationControls.tsx # Route optimization controls
│   ├── services/
│   │   └── api.ts                # API client
│   ├── types/
│   │   └── index.ts              # TypeScript types
│   ├── App.tsx                   # Main application component
│   └── App.css                   # Styles
├── public/                       # Static assets
└── package.json                  # Dependencies
```

## 🎯 Usage

1. **Add Bus Stops**: Click anywhere on the map to add a new bus stop
2. **Edit Stops**: Click on existing stops to edit them
3. **Optimize Routes**: Set the number of buses and click "Optimize Routes"
4. **View Results**: See the optimized routes as colored lines on the map

## 🛠️ Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### API Endpoints Used

- `GET /api/v1/stops/` - Get all bus stops
- `POST /api/v1/stops/` - Create bus stop
- `PUT /api/v1/stops/{id}` - Update bus stop
- `DELETE /api/v1/stops/{id}` - Delete bus stop
- `POST /api/v1/optimize/routes` - Optimize routes

## 🐛 Troubleshooting

### Common Issues

1. **Map not loading**: Check your Google Maps API key in `.env`
2. **API errors**: Ensure the backend is running on port 8000
3. **CORS errors**: The backend should have CORS configured for localhost:3000

### Browser Console

Check the browser console for detailed error messages and API responses.