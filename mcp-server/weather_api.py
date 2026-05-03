import httpx
from typing import Dict, Any, Optional

async def get_coordinates(city_name: str) -> Optional[Dict[str, float]]:
    """Get coordinates (lat, lon) for a city name using Open-Meteo Geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "lat": result["latitude"],
                "lon": result["longitude"],
                "name": result["name"],
                "country": result.get("country", "")
            }
    return None

async def get_weather_forecast(lat: float, lon: float) -> Dict[str, Any]:
    """Get current and hourly weather forecast from Open-Meteo."""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code"
        f"&timezone=auto"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

def get_weather_description(code: int) -> str:
    """Map WMO Weather Interpretation Codes to human-readable strings."""
    # Simplified WMO codes mapping
    mapping = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return mapping.get(code, "Unknown")
