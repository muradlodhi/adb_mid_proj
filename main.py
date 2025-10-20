cat << 'EOF' > main.py
# main.py
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from datetime import datetime, timezone
from typing import List, Optional
from models import LocationUpdate, FlightLog, PathPoint # <-- Import Schemas

# --- CONFIGURATION (PLACEHOLDER) ---
MONGO_URI = "mongodb+srv://mur:mur@cluster0.r1rpnj6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "FlightTrackerDB"
CURRENT_COLLECTION_NAME = "current_flight_locations"
LOG_COLLECTION_NAME = "flight_logs"
# -----------------------------------

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    current_collection = db[CURRENT_COLLECTION_NAME]
    log_collection = db[LOG_COLLECTION_NAME]
    print("MongoDB connection established.")
except Exception as e:
    # This prevents the app from starting if the DB is unreachable
    raise Exception(f"Failed to connect to MongoDB: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="Flight Tracking API (FastAPI + MongoDB)",
    version="1.0.0",
    description="API for ingesting real-time flight location data and retrieving flight history."
)

# --- UTILITY FUNCTION ---
def log_completed_flight(flight_id: str):
    """
    Retrieves all current locations, compiles them into one log document, and deletes tracking data.
    """
    path_documents = list(current_collection.find({"flightId": flight_id}, projection={"_id": 0}).sort("timestamp", 1))
    
    if not path_documents:
        return "Flight path not found in current tracking.", False

    path_details = []
    for doc in path_documents:
        path_point_data = {
            "lat": doc["latitude"],
            "lon": doc["longitude"],
            "alt": doc.get("altitude", 0),
            "ts": doc["timestamp"]
        }
        point = PathPoint(**path_point_data).model_dump(by_alias=True)
        path_details.append(point)

    log_entry = FlightLog(
        flightId=flight_id,
        departureTime=path_documents[0]["timestamp"],
        arrivalTime=path_documents[-1]["timestamp"],
        path=path_details,
        logged_at=datetime.now(timezone.utc)
    ).model_dump(by_alias=True, exclude_none=True)

    try:
        log_collection.insert_one(log_entry)
        current_collection.delete_many({"flightId": flight_id})
        return "Flight logged and tracking cleared successfully.", True
    except Exception as e:
        print(f"MongoDB Insert Error: {e}")
        return f"Error during logging: {e}", False

# --- ENDPOINTS ---

@app.post("/api/v1/update-location", tags=["Ingestion"])
async def ingest_location_update(update: LocationUpdate):
    """
    Receives a single real-time location update. Triggers logging if destinationReached is True.
    """
    update_data = update.model_dump()
    destination_reached = update_data.pop("destinationReached")

    try:
        current_collection.insert_one(update_data)
        
        if destination_reached:
            log_message, success = log_completed_flight(update.flightId)
            if success:
                return {"message": "Location updated and flight logged successfully.", "log_status": log_message}
            else:
                raise HTTPException(status_code=500, detail=f"Location updated, but logging failed: {log_message}")
        else:
            return {"message": "Location updated successfully."}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database operation failed: {e}")

@app.get("/api/v1/track/{flight_id}", tags=["Retrieval"], response_model=Optional[FlightLog])
async def track_flight(
    flight_id: str,
    all_path: bool = Query(False, description="Set to True to retrieve the full path from historical logs."),
    timestamp: Optional[datetime] = Query(None, description="Request the location closest to this time (only valid if all_path is False).")
):
    """
    Retrieves the latest location for an active flight, or the full path for a completed flight.
    """
    if all_path:
        # Retrieve Full Path from Logs
        log_document = log_collection.find_one({"flightId": flight_id}, projection={"_id": 0})
        if log_document:
            return FlightLog(**log_document)
        else:
            raise HTTPException(status_code=404, detail=f"Flight {flight_id} path not found in historical logs.")
    else:
        # Retrieve Latest Location from Current Tracking
        query = {"flightId": flight_id}
        if timestamp:
            query["timestamp"] = {"$lte": timestamp}
            sort_order = -1
        else:
            sort_order = -1 

        latest_update = current_collection.find_one(
            query, 
            sort=[("timestamp", sort_order)],
            projection={"_id": 0}
        )

        if latest_update:
            # Return a simple dictionary for the latest point
            return {
                "flightId": latest_update["flightId"],
                "latitude": latest_update["latitude"],
                "longitude": latest_update["longitude"],
                "altitude": latest_update["altitude"],
                "timestamp": latest_update["timestamp"],
                "status": latest_update.get("status", "En Route")
            }
        else:
            raise HTTPException(status_code=404, detail=f"Flight {flight_id} currently not being tracked or not found at the requested time.")

# To run the app, execute: uvicorn main:app --reload
EOF