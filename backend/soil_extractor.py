import json
from io import BytesIO
from PIL import Image
from google import genai

def extract_soil_data_from_image(image_bytes: bytes) -> dict:
    """
    Extracts N, P, K, pH, and location from a soil test report image using Gemini.
    """
    try:
        client = genai.Client()
        image = Image.open(BytesIO(image_bytes))
        
        prompt = (
            "Analyze this soil test report image and extract:\n"
            "- N (Nitrogen) as float\n"
            "- P (Phosphorus) as float\n"
            "- K (Potassium) as float\n"
            "- pH as float\n"
            "- Location (City, District, or Region name if printed on report, otherwise null)\n\n"
            "Return ONLY a valid JSON object with these exact keys: "
            '{"N": 0.0, "P": 0.0, "K": 0.0, "pH": 0.0, "location": null}'
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image, prompt],
        )
        
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
            
        data = json.loads(response_text)
        return {
            "N": float(data.get("N", 50.0)),
            "P": float(data.get("P", 50.0)),
            "K": float(data.get("K", 50.0)),
            "pH": float(data.get("pH", 6.5)),
            "location": data.get("location")
        }
    except Exception as e:
        print(f"⚠️ Gemini OCR extraction failed: {e}. Using defaults.")
        return {"N": 50.0, "P": 50.0, "K": 50.0, "pH": 6.5, "location": None}
