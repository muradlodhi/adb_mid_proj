cat << 'EOF' > models.py
# models.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# 📐 Pydantic Model for a single location update (POST body)
class LocationUpdate(BaseModel):
    flightId: str = Field(..., example="UA1234", description="Unique identifier for the flight.")
    latitude: float = Field(..., ge=-90, le=90, example=40.7128, description="Current latitude.")
    longitude: float = Field(..., ge=-180, le=180, example=-74.0060, description="Current longitude.")
    altitude: int = Field(default=0, ge=0, example=35000, description="Current altitude in feet.")
    timestamp: datetime = Field(..., description="Time the signal was recorded (ISO 8601 format, UTC preferred).")
    status: str = Field(default="En Route", example="En Route", description="Current flight status (e.g., Departed, Landed).")
    destinationReached: bool = Field(default=False, description="Set to true to trigger permanent logging and clear tracking data.")

# 🗺️ Pydantic Model for a single point in a historical path
class PathPoint(BaseModel):
    lat: float = Field(..., description="Latitude.")
    lon: float = Field(..., description="Longitude.")
    alt: int = Field(default=0, description="Altitude in feet.")
    ts: datetime = Field(..., description="Timestamp of the recording.")

# 📜 Pydantic Model for a completed (logged) flight (GET response)
class FlightLog(BaseModel):
    flightId: str
    departureTime: datetime
    arrivalTime: datetime
    path: List[PathPoint]
    logged_at: datetime = Field(..., description="Time the flight record was finalized in the system.")
EOF