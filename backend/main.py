import os
import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai

from backend.weather_api import get_weather_data
from backend.soil_extractor import extract_soil_data_from_image

app = FastAPI(
    title="Smart Farming Pipeline API",
    description="API for multi-crop recommendation using soil report OCR, live climate data, and ML probabilities.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained ML model at startup
MODEL_PATH = os.path.join("ml", "model.pkl")
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "model.pkl"

model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ Loaded trained crop recommendation model successfully.")
else:
    print("⚠️ Warning: model.pkl not found! Train your model first using ml/train.py.")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Smart Farming Pipeline API v2.0 is running."}

@app.post("/predict-crop")
@app.post("/predict-crop/")
async def predict_crop(file: UploadFile = File(...)):
    """
    Accepts ONLY a soil report image file, extracts metrics via Gemini OCR,
    fetches live climate data via Open-Meteo, predicts the top 3 recommended crops,
    and returns Gemini's agronomic analysis.
    """
    if not model:
        raise HTTPException(status_code=500, detail="ML model is not loaded on the server.")
    
    try:
        # 1. Read uploaded soil report image bytes
        image_bytes = await file.read()
        
        # 2. Extract soil properties & location using Gemini OCR
        soil_data = extract_soil_data_from_image(image_bytes)
        
        # Default baseline coordinates for weather API integration
        lat, lon = 17.3850, 78.4867 
        
        # 3. Fetch live weather (temperature & rainfall) from Open-Meteo API
        weather_data = get_weather_data(lat, lon)
        temperature = weather_data["temperature"]
        rainfall = weather_data["rainfall"]
        
        # 4. Construct feature dataframe matching training columns
        input_features = pd.DataFrame([{
            'N': soil_data['N'],
            'P': soil_data['P'],
            'K': soil_data['K'],
            'temperature': temperature,
            'pH': soil_data['pH'],
            'rainfall': rainfall
        }])
        
        # 5. Predict Top 3 Crops using model probabilities
        probabilities = model.predict_proba(input_features)[0]
        classes = model.classes_
        
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_3_crops = [
            {
                "crop": str(classes[i]),
                "confidence_score": round(float(probabilities[i]) * 100, 2)
            }
            for i in top_indices
        ]
        
        # 6. Generate Gemini Agronomic Recommendation & Analysis with explicit API key handling
        api_key = os.environ.get("AQ.Ab8RN6KqR8SqLBPw3ZyNnfVbmies1dYf-sT3IkrcU7hEZYMp3w")
        client = genai.Client(api_key=api_key) if api_key else genai.Client()
        
        prompt = (
            f"Given the following agricultural parameters:\n"
            f"- Nitrogen (N): {soil_data['N']}\n"
            f"- Phosphorus (P): {soil_data['P']}\n"
            f"- Potassium (K): {soil_data['K']}\n"
            f"- pH: {soil_data['pH']}\n"
            f"- Temperature: {temperature}°C\n"
            f"- Rainfall: {rainfall}mm\n"
            f"- Top Recommended Crops: {', '.join([c['crop'] for c in top_3_crops])}\n\n"
            "Provide a brief, professional 2-3 sentence agronomic insight explaining why these crops suit these conditions and any quick fertilizer tips."
        )
        
        gemini_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        ai_insights = gemini_response.text.strip()
        
        return {
            "status": "success",
            "top_3_recommendations": top_3_crops,
            "inputs_detected": {
                "soil_metrics": {k: soil_data[k] for k in ["N", "P", "K", "pH"]},
                "detected_location": soil_data.get("location"),
                "climate_metrics": {
                    "temperature": temperature,
                    "rainfall": rainfall
                }
            },
            "gemini_agronomic_insights": ai_insights
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
