from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

# Define path to CSV file
CSV_FILE_PATH = r"C:\Users\NabeelOverEasy\OneDrive - Over Easy Solar AS\Demo Html\1\Solardata_1.csv"

# Load CSV Data
df = pd.read_csv(CSV_FILE_PATH)
df.fillna(0, inplace=True)  # Replace NaN with zero

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to find the nearest coordinate
def find_nearest(lat, lon):
    df["distance"] = ((df["Latitude"] - lat) ** 2 + (df["Longitude"] - lon) ** 2)
    nearest_row = df.loc[df["distance"].idxmin()]
    return nearest_row

@app.get("/get_solar_data")
def get_solar_data(lat: float = Query(...), lon: float = Query(...)):
    nearest = find_nearest(lat, lon)

    return {
        "GHI": nearest["GHI"],
        "DNI": nearest["DNI"],
        "DIF": nearest["DIF"],
        "TEMP": nearest["TEMP"]
    }

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
