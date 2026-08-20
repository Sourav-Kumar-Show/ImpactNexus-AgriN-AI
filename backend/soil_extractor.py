import os
import json
from io import BytesIO
from PIL import Image
from google import genai

def extract_soil_data_from_image(image_bytes: bytes) -> dict:
    """
    Uses Gemini Multimodal capability via PIL and the google-genai SDK 
    to extract N, P, K, and pH values from uploaded soil report images.
    """
    try:
        # Initialize client (picks up GEMINI_API_KEY from environment)
        client = genai.Client()
        
        # Open image from bytes
        image = Image.open(BytesIO(image_bytes))
        
        prompt = (
            "Extract the N (Nitrogen), P (Phosphorus), K (Potassium), "
            "and pH values from this soil report image. "
            "Return ONLY a valid JSON object with numeric values for these exact keys: "
            '{"N": 0.0, "P": 0.0, "K": 0.0, "pH": 0.0}'
        )
        
        print("Sending soil report image to Gemini for OCR extraction...")
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[image, prompt],
        )
        
        response_text = response.text.strip()
        print(f"Gemini raw response: {response_text}")
        
        # Clean markdown code formatting if present
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
            
        data = json.loads(response_text)
        
        extracted = {
            "N": float(data.get("N", 50.0)),
            "P": float(data.get("P", 50.0)),
            "K": float(data.get("K", 50.0)),
            "pH": float(data.get("pH", 6.5))
        }
        print(f"Successfully extracted soil metrics: {extracted}")
        return extracted
        
    except Exception as e:
        print(f"⚠️ Gemini OCR extraction failed: {e}. Using fallback soil metrics.")
        return {"N": 50.0, "P": 50.0, "K": 50.0, "pH": 6.5}
