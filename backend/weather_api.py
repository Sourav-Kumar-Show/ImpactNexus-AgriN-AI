import requests

def get_weather_data(lat: float, lon: float) -> dict:
    """
    Fetches real-time temperature and rainfall data for given coordinates
    using the free Open-Meteo API, with built-in fallback values.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "precipitation"],
        "timezone": "auto"
    }
    
    # Default fallback values if the API call fails
    fallback_data = {
        "temperature": 25.0,
        "rainfall": 100.0
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        temperature = current.get("temperature_2m", fallback_data["temperature"])
        rainfall = current.get("precipitation", fallback_data["rainfall"])
        
        # If precipitation returns hourly mm, scale or handle appropriately 
        # (or use fallback if values are missing)
        return {
            "temperature": float(temperature) if temperature is not None else fallback_data["temperature"],
            "rainfall": float(rainfall) if rainfall is not None else fallback_data["rainfall"]
        }
        
    except Exception as e:
        print(f"⚠️ Weather API fetch failed: {e}. Using fallback values.")
        return fallback_data

if __name__ == "__main__":
    # Quick test for Secunderabad / regional coordinates
    test_lat, test_lon = 17.4399, 78.4983
    print("Testing weather fetch:", get_weather_data(test_lat, test_lon))