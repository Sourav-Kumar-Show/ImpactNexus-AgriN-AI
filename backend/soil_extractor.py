import os
import json
import time
import traceback
from io import BytesIO
from PIL import Image
from google import genai

def extract_soil_data_from_image(image_bytes: bytes) -> dict:
    """
    Extracts N, P, K, pH, and location from a soil test report image using Gemini 
    with built-in retry logic for temporary service spikes.
    """
    api_key = os.environ.get("AQ.Ab8RN6KqR8SqLBPw3ZyNnfVbmies1dYf-sT3IkrcU7hEZYMp3w")
    client = genai.Client(api_key=api_key) if api_key else genai.Client()
    
    image = Image.open(BytesIO(image_bytes))
    
    prompt = (
        "Analyze this soil test report image and extract the exact numerical values for:\n"
        "- N (Nitrogen) as float\n"
        "- P (Phosphorus) as float\n"
        "- K (Potassium) as float\n"
        "- pH as float\n"
        "- Location (City or Region name if printed, otherwise null)\n\n"
        "Return ONLY a valid JSON object with these exact keys: "
        '{"N": 0.0, "P": 0.0, "K": 0.0, "pH": 0.0, "location": null}'
    )
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"🔍 Sending soil report image to Gemini OCR (Attempt {attempt + 1}/{max_retries})...")
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[image, prompt],
            )
            
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()
                
            data = json.loads(response_text)
            extracted = {
                "N": float(data.get("N", 50.0)),
                "P": float(data.get("P", 50.0)),
                "K": float(data.get("K", 50.0)),
                "pH": float(data.get("pH", 6.5)),
                "location": data.get("location")
            }
            print(f"✅ Successfully parsed soil metrics: {extracted}")
            return extracted
            
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                print("⚠️ All Gemini OCR retries exhausted. Falling back to default baseline values.")
                
    return {"N": 50.0, "P": 50.0, "K": 50.0, "pH": 6.5, "location": None}
