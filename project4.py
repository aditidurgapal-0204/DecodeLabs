import os
import httpx
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

# 1. THE VAULT: Pulling credentials securely from local environment variables (Slide 3)
EXTERNAL_API_KEY = os.getenv("WEATHER_API_KEY", "fallback_local_dev_key")
EXTERNAL_API_URL = "https://api.weatherapi.com/v1/current.json"  # Simulated weather provider base url

# --- TRANSLATOR SCHEMAS ---
# This is the minimal, semantic "Client Parcel" our frontend actually needs (Slide 5)
class CleanWeatherResponse(BaseModel):
    city: str
    temperature_celsius: float
    humidity: int
    condition: str
    status: str

# --- 4. THE SHIELD: Fallback structural template for graceful degradation (Slide 7)
def get_graceful_fallback_data(city: str, reason: str) -> CleanWeatherResponse:
    return CleanWeatherResponse(
        city=city.title(),
        temperature_celsius=0.0,
        humidity=0,
        condition="Data temporarily unavailable",
        status=f"Graceful Degradation: {reason}"
    )

# --- THE MESSENGER ENGINE (Slide 4 & 5) ---
@router.get("/weather/{city}", response_model=CleanWeatherResponse)
async def get_weather(city: str):
    """
    Acts as a secure backend proxy middleware.
    Fetches, translates, and shields data from an external provider.
    """
    # 2. THE MESSENGER: Non-blocking async networking context manager (equivalent to Axios)
    # 4. THE SHIELD: Applying strict timeout bounds (5000ms limit) to block resource starvation (Slide 7)
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            # Dispatch request with credentials hidden safely behind our firewall (Slide 3)
            # (Using a public testing sandbox query string setup for mock execution)
            response = await client.get(
                "https://wttr.in/{}?format=j1".format(city)
            )
            
            # 4. THE SHIELD: Catching 4xx/5xx network response code errors from the provider
            if response.status_code >= 400:
                return get_graceful_fallback_data(city, f"Upstream provider returned HTTP {response.status_code}")
                
            raw_data = response.json()
            
            # 3. THE TRANSLATOR: Filtering out 100+ parameters of noise into 5 clean fields (Slide 5)
            current_condition = raw_data['current_condition'][0]
            nearest_area = raw_data['nearest_area'][0]
            
            translated_parcel = CleanWeatherResponse(
                city=nearest_area['areaName'][0]['value'].title(),
                temperature_celsius=float(current_condition['temp_C']),
                humidity=int(current_condition['humidity']),
                condition=current_condition['weatherDesc'][0]['value'],
                status="Success: Real-time Data Secured"
            )
            
            return translated_parcel
            
        # 4. THE SHIELD: Containing hardware dropouts and connection timeouts safely (Slide 7)
        except httpx.TimeoutException:
            return get_graceful_fallback_data(city, "Network Timeout spiked over 5000ms limit.")
        except Exception as e:
            return get_graceful_fallback_data(city, "Unhandled internal gateway variance.")