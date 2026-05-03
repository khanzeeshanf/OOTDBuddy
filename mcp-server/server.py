from fastmcp import FastMCP
import weather_api
import asyncio
from datetime import datetime, timedelta

# Initialize FastMCP server
mcp = FastMCP("OOTDBuddy")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city."""
    coords = await weather_api.get_coordinates(city)
    if not coords:
        return f"Could not find location for city: {city}"
    
    weather = await weather_api.get_weather_forecast(coords["lat"], coords["lon"])
    current = weather.get("current_weather", {})
    temp = current.get("temperature", "N/A")
    code = current.get("weathercode", 0)
    desc = weather_api.get_weather_description(code)
    
    return f"Current weather in {coords['name']}, {coords['country']}: {temp}°C, {desc}."

@mcp.tool()
async def recommend_ootd(city: str, duration_hours: int = 4) -> str:
    """
    Suggest what to wear and carry based on the forecast for a specific duration.
    
    Args:
        city: The city name.
        duration_hours: How many hours you plan to be outside (default 4).
    """
    coords = await weather_api.get_coordinates(city)
    if not coords:
        return f"Could not find location for city: {city}"
    
    weather = await weather_api.get_weather_forecast(coords["lat"], coords["lon"])
    
    # Analyze forecast for the next 'duration_hours'
    hourly = weather.get("hourly", {})
    temps = hourly.get("temperature_2m", [])[:duration_hours]
    precip_prob = hourly.get("precipitation_probability", [])[:duration_hours]
    precip_amount = hourly.get("precipitation", [])[:duration_hours]
    codes = hourly.get("weather_code", [])[:duration_hours]
    
    if not temps:
        return "Forecast data not available."
    
    avg_temp = sum(temps) / len(temps)
    max_precip_prob = max(precip_prob) if precip_prob else 0
    total_precip = sum(precip_amount) if precip_amount else 0
    
    # Decision logic
    suggestions = []
    
    # Temperature based suggestions
    if avg_temp < 10:
        suggestions.append("It's quite cold. Wear a heavy jacket, gloves, and a scarf.")
    elif avg_temp < 18:
        suggestions.append("Mildly cold. A light jacket or sweater would be perfect.")
    elif avg_temp < 25:
        suggestions.append("Comfortable weather. Light cotton clothes are recommended.")
    else:
        suggestions.append("It's hot! Wear loose, breathable cotton clothes and stay hydrated.")
        
    # Rain/Precipitation based suggestions
    if max_precip_prob > 50 or total_precip > 0.5:
        suggestions.append("High chance of rain. Definitely carry an umbrella or wear a raincoat.")
    elif max_precip_prob > 20:
        suggestions.append("Slight chance of rain. You might want to carry a compact umbrella just in case.")
        
    # Sun protection (based on weather codes for clear sky/mainly clear)
    is_sunny = any(c in [0, 1] for c in codes)
    if is_sunny and avg_temp > 20:
        suggestions.append("It might be sunny. Don't forget your sunglasses and a cap.")

    summary = (
        f"--- OOTD Buddy Report for {coords['name']} ---\n"
        f"Forecast for next {duration_hours} hours:\n"
        f"Avg Temp: {avg_temp:.1f}°C\n"
        f"Max Rain Probability: {max_precip_prob}%\n\n"
        f"Recommendations:\n- " + "\n- ".join(suggestions)
    )
    
    return summary

@mcp.resource("ootd://style-guide")
def get_style_guide() -> str:
    """Get a guide on clothing materials and weather suitability."""
    return """
    # OOTDBuddy Style & Material Guide
    
    ## Temperature Guidelines:
    - Above 25°C: Use Linen, Seersucker, or Lightweight Cotton.
    - 15°C to 25°C: Standard Cotton, Jersey, or Light Knits.
    - 5°C to 15°C: Wool, Flannel, Denim, or Layered Fleece.
    - Below 5°C: Down/Insulated synthetics, Thermal base layers, and Heavy Wool.
    
    ## Rain Protection:
    - Light Rain: Water-resistant (DWR) treated fabrics.
    - Heavy Rain: Waterproof membranes (Gore-Tex) or Vinyl.
    
    ## Wind:
    - High Wind: Wind-resistant shells (Nylon/Polyester blends).
    """

@mcp.prompt("plan-my-trip")
def plan_trip_prompt(city: str) -> str:
    """A prompt template to help you plan an outfit for a trip."""
    return f"I'm planning a trip to {city}. Can you use the OOTDBuddy tools to check the weather for the next 8 hours and suggest a full outfit using the style guide resource? Please include specific fabric recommendations."

if __name__ == "__main__":
    mcp.run()
