# AgriNexus Frontend

A polished React prototype for **AgriNexus**, an AI-driven agricultural intelligence platform. It brings farm health, satellite and soil signals, AI advice, crop disease checks, and the BRICS interoperability concept into one responsive SaaS-style interface.

## Technology

- React 19 + Vite
- React Router for the five application routes
- Recharts for NDVI and weather visualizations
- Lucide React for icons
- Responsive CSS-based UI
- Native `fetch` API service for the FastAPI backend

## Run locally

```bash
npm install
npm run dev
```

Open the local URL printed by Vite (normally `http://localhost:5173`).

```bash
npm run build
npm run lint
npm run preview
```

## Screens

The frontend intentionally contains exactly five main screens.

### 1. Dashboard (`/dashboard`)

Daily overview for `farm-001`.

- Farm Health radial score
- NDVI, soil moisture, temperature, and disease-risk cards
- AI recommendation hero card linked to the full advisory
- NDVI trend area chart and seven-day weather outlook chart
- Vegetation, soil, and disease quick insights
- Last-updated and API connection indicators

### 2. Farm Intelligence (`/intelligence`)

The data layer behind farm analysis.

- Stylized farm boundary map for Nashik, Maharashtra, India
- Farm ID and crop context
- Satellite metrics: NDVI, EVI, SAVI, NDMI, and cloud cover
- Vegetation-health interpretation
- Weather: temperature, humidity, rainfall, wind, and forecast
- Soil: pH, organic carbon, moisture, NPK, and health radial score
- Satellite, weather, and soil data-source indicator

### 3. AI Advisory (`/advisory`)

The action-oriented intelligence center.

- Water-stress, heat-stress, disease-risk, and yield-risk overview
- Action cards with category and priority
- Feature-importance visualization for NDVI, soil moisture, rainfall, and temperature
- Decision pipeline from field signals to farmer advisory
- Crop Doctor call to action

### 4. Crop Doctor (`/doctor`)

AI computer-vision styled disease diagnosis workflow.

- PNG, JPG, and JPEG file selection
- Image preview, filename, and size
- Multipart upload using the `leaf_image` field
- Analysis loading state and completion toast
- Disease result with confidence radial indicator, severity, symptoms, and next action
- “Analyze Another Image” reset flow and professional empty state

### 5. BRICS Network (`/brics`)

Cross-border agricultural interoperability prototype.

- Network visualization for India, Brazil, China, Russia, and South Africa
- AgriNexus Interoperability Layer hub
- Country model registry table
- Dynamic BRICS-AGRI-SCHEMA fields and version
- Data sovereignty flow from local processing to anonymised insights
- Demonstration-only sharing controls and raw-data-local notice

## Shared experience

- Persistent desktop sidebar with active navigation
- Mobile navigation drawer and tablet-aware layouts
- Top bar showing farm, location, crop, profile, notifications, and API status
- Reusable cards, badges, progress bars, metrics, buttons, and chart layouts
- Agriculture-inspired green design with responsive charts and mobile table scrolling
- API error state with retry control

## FastAPI integration

The API client is at [`src/services/api.js`](src/services/api.js) and targets:

```text
https://impactnexus-backend.onrender.com
```

| Feature | Method | Endpoint |
| --- | --- | --- |
| Farm context | GET | `/api/farm/farm-001` |
| Farm intelligence | GET | `/api/farm/farm-001/intelligence` |
| AI advisory | GET | `/api/farm/farm-001/advisory` |
| Crop Doctor | POST multipart/form-data | `/api/crop-doctor` |
| BRICS models | GET | `/api/brics/models` |
| BRICS schema | GET | `/api/brics/schema` |

Crop Doctor sends the selected image as `leaf_image`.

## Prototype fallback behavior

Live FastAPI data is used whenever available. If an API request fails, the relevant UI remains demonstrable with structured fallback farm intelligence, recommendations, BRICS data, or a clearly labelled demo crop diagnosis. The UI shows an offline message and retry button; it never modifies backend data.

## Project structure

```text
src/
├── App.jsx              # Layout, routes, pages, and reusable UI pieces
├── index.css            # Design system and responsive styles
├── main.jsx             # React and router bootstrap
└── services/
    └── api.js           # Central FastAPI client
```

## Scope

This frontend prototype does not add authentication, payments, real satellite/weather/soil providers, real ML inference, persistent data sharing, or a real BRICS network. It represents these concepts through a professional interactive interface suitable for a demo or hackathon presentation.
