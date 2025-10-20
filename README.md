**Name      :  Murad Lodhi**   
**Reg#     :  FA23-BCS-145**   
**Section   :  C**   

# **Advanced Databsase**
**Midterm Project Group: E**

# ✈️ FastAPI Flight Tracking API

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)
![Database](https://img.shields.io/badge/Database-MongoDB-47A248.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg)

A high-performance **RESTful API** built using **FastAPI** and **MongoDB** for real-time flight tracking.  
This API can ingest, store, and retrieve flight data, with automatic transition from active tracking to historical logging when flights reach their destination.

---

## 🚀 Overview

This project demonstrates a scalable backend system for flight data management using:
- **FastAPI** for ultra-fast asynchronous APIs
- **Pydantic v2** for strong schema validation
- **MongoDB** for flexible NoSQL persistence

It includes automatic flight logging, real-time ingestion, and retrieval endpoints for active and completed flights.

---

## ✨ Key Features

✅ **Real-Time Flight Data Ingestion** – `POST` endpoint to update or insert new flight location data  
✅ **Automatic Historical Logging** – Moves flights from active tracking to logs when `destinationReached=True`  
✅ **Historical Retrieval** – Fetch full flight paths from historical logs  
✅ **Active Flight Lookup** – Retrieve the latest position for any ongoing flight  
✅ **Interactive API Docs** – Built-in Swagger UI (`/docs`) and ReDoc (`/redoc`)  

---

## 🗂️ Project Structure

```
flight-tracker-api/
│
├── app/
│   ├── main.py                # Main FastAPI app with routes and logic
│   ├── models.py              # Pydantic schemas for data validation
│   ├── database/
│   │   └── connection.py      # MongoDB connection setup
│   └── services/
│       └── flight_service.py  # Business logic (optional separation)
│
├── requirements.txt           # Dependencies list
├── .env.example               # Environment variable template
├── .gitignore                 # Ignored files and folders
└── README.md                  # Project documentation
```

---

## ⚙️ Setup & Installation

### 1️⃣ Prerequisites
- Python **3.8+**
- A **MongoDB Atlas** or local MongoDB instance
- Git installed locally

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/flight-tracker-api.git
cd flight-tracker-api
```

### 3️⃣ Create Virtual Environment
**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```
**Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Setup Environment Variables
Copy `.env.example` to `.env` and update your MongoDB URI and database name:
```
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
DATABASE_NAME=FlightTrackerDB
```

### 6️⃣ Run the Server
```bash
uvicorn app.main:app --reload
```

Visit:
> 🔗 http://127.0.0.1:8000/docs — Swagger UI  
> 🔗 http://127.0.0.1:8000/redoc — ReDoc documentation  

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/api/v1/update-location` | Ingests new flight data (real-time updates) |
| `GET` | `/api/v1/track/{flight_id}` | Retrieves flight details (active or historical) |

### Example Request
**POST /api/v1/update-location**
```json
{
  "flightId": "PK303",
  "latitude": 31.5204,
  "longitude": 74.3587,
  "altitude": 32000,
  "speed": 890,
  "destinationReached": false,
  "timestamp": "2025-10-20T18:23:00Z"
}
```

When `"destinationReached": true`, the flight is logged to history automatically.

---

## 🧰 Tech Stack

- **FastAPI** – async web framework  
- **MongoDB + PyMongo** – database and client driver  
- **Pydantic v2** – data validation models  
- **Uvicorn** – ASGI server for development  

---

## 🧑‍💻 Author

**Your Name**  
📧 your.email@example.com  
🌐 [github.com/your-username](https://github.com/your-username)

---

## 🪪 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it for both personal and commercial use.

---

## ⭐ Contribute

If you find this project useful:
1. Star 🌟 the repository  
2. Fork 🍴 and make improvements  
3. Submit a Pull Request 🤝  

> “Simple, fast, and efficient flight tracking – powered by FastAPI.”
