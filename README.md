# ImpactNexus-AgriN-AI

Real-time agro-advisor that recommends regenerative practices from satellite, soil, and weather signals, plus a leaf-photo diagnostic. Advisory and Crop Doctor use Gemini Flash through the Google AI Studio API.

## Google AI

`GET /api/farm/{farm_id}/advisory` sends the farm signals to Gemini and returns risks, regenerative actions, and feature importance. `POST /api/crop-doctor` sends the leaf photo to Gemini vision.

Calls stay on the free tier:

- Model is Gemini Flash. Pro model names are ignored.
- Output is capped, thinking is kept minimal, and each request is attempted once.
- An advisory is cached for 12 hours. The same leaf photo is cached for 7 days.
- `GEMINI_DAILY_CALL_BUDGET` defaults to 30 Gemini attempts per day, including failed attempts. After that, the API serves demo guidance and does not call Google.
- A failed call is remembered for 10 minutes so a refresh loop does not spend the budget.

The key is read from the environment. It is never committed.

### Local key

Create `backend/.env` from `backend/.env.example`:

```bash
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash
GEMINI_DAILY_CALL_BUDGET=30
```

Create the key in [Google AI Studio](https://aistudio.google.com/) with the hackathon Google account. Leave billing off.

### Render

The live frontend calls `https://impactnexus-backend.onrender.com`. The teammate who owns that Render service adds `GEMINI_API_KEY` under **Environment** and redeploys. Until that variable exists, the deployed site keeps returning demo guidance. Local runs use `backend/.env`.

## Run

```bash
cd backend
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/uvicorn main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

Guard tests do not call Gemini:

```bash
cd backend
venv/bin/python -m unittest test_gemini_guard.py
```

## Open-source components

- [React](https://github.com/facebook/react) (MIT), [Vite](https://github.com/vitejs/vite) (MIT), [React Router](https://github.com/remix-run/react-router) (MIT)
- [Recharts](https://github.com/recharts/recharts) (MIT), [Lucide](https://github.com/lucide-icons/lucide) (ISC)
- [FastAPI](https://github.com/fastapi/fastapi) (MIT), [Uvicorn](https://github.com/encode/uvicorn) (BSD-3-Clause), [Pydantic](https://github.com/pydantic/pydantic) (MIT)
- [google-genai](https://github.com/googleapis/python-genai) (Apache-2.0), [Pillow](https://github.com/python-pillow/Pillow) (HPND), [python-dotenv](https://github.com/theskumar/python-dotenv) (BSD-3-Clause)
