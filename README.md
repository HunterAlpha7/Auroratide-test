# AuroraTide: AI-Driven Flood Prediction Service

## Project Overview
AuroraTide is a full-stack AI-powered flood prediction service. It provides district-level flood risk predictions via a FastAPI backend and visualizes them on an interactive React-based map frontend. The system is designed for rapid deployment and easy integration, with robust fallback behavior if data is missing.

---

## Backend (API) Setup

### Dependencies
- Python 3.8+
- fastapi
- uvicorn
- scikit-learn
- pandas
- joblib

### Installation
```bash
# Clone the repository and navigate to the project root
pip install -r requirements.txt
```

### Running the Backend
```bash
uvicorn api_service:app --reload
```
- The API will be available at: `http://127.0.0.1:8000`
- Main endpoint: `GET /predict_all`

### API Endpoint
- **GET /predict_all**
  - Returns: JSON with flood risk probabilities for all 64 districts of Bangladesh.
  - Example response:
    ```json
    {
      "predictions": [
        {"district": "Dhaka", "probability": 0.12},
        {"district": "Chattogram", "probability": 0.03},
        ...
      ]
    }
    ```
- If the model or data is missing, the API returns 0 probability for all districts (no errors).

---

## Frontend (React) Setup

### Dependencies
- Node.js 18+
- npm
- axios
- react
- react-dom
- react-scripts or vite (recommended)
- react-simple-maps
- d3-scale, d3-scale-chromatic

### Installation
```bash
# In the project root, create the frontend folder
cd ..
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install axios react-simple-maps d3-scale d3-scale-chromatic
```

### Running the Frontend
```bash
npm run dev
```
- The app will be available at: `http://localhost:5173` (or as shown in your terminal)

### Map Data
- The frontend fetches Bangladesh district boundaries from an online GeoJSON provider (see below for details).
- No manual download is required.

---

## Usage Guide
1. **Start the backend API:**
   - `uvicorn api_service:app --reload`
2. **Start the frontend React app:**
   - `cd frontend && npm run dev`
3. **Open your browser:**
   - Go to `http://localhost:5173`
   - You will see a map of Bangladesh with each district colored by flood risk probability.
   - Hover over a district to see its name and risk percentage.

---

## Data & Model Notes
- The backend expects a trained model at `data/rf_flood_model_24_48h.joblib`.
- If the model or data is missing, the API will return 0 probability for all districts (safe fallback).
- The system is designed to work only for Bangladesh districts.

---

## Troubleshooting
- **CORS Issues:** If the frontend cannot fetch from the backend, ensure both are running on the correct ports and consider enabling CORS in FastAPI if needed.
- **Port Conflicts:** Default ports are 8000 (backend) and 5173 (frontend). Change as needed.
- **GeoJSON/Map Issues:** The frontend uses an online GeoJSON source for Bangladesh districts. No manual download is needed.
