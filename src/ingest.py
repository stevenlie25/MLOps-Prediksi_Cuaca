"""
Data Ingestion Script for Weather Data.
Fetches dynamic weather data from Open-Meteo API for Malang area
and saves it into data/raw with a timestamp to prevent overwriting.
"""

import os
import sys
from datetime import datetime
import pandas as pd
import requests


def fetch_weather_data() -> None:
    """Fetch weather data from Open-Meteo API and save as a timestamped CSV."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -7.9839,  # Latitude Malang
        "longitude": 112.6214,  # Longitude Malang
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "surface_pressure",
            "wind_speed_10m",
            "precipitation",
        ],
        "timezone": "Asia/Jakarta",
        "past_days": 2,  # Historical dynamic data
    }

    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time_str}] Mengirim request ke Open-Meteo API...")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data["hourly"])
        df["time"] = pd.to_datetime(df["time"])

        # Buat direktori data/raw jika belum ada
        output_dir = os.path.join("data", "raw")
        os.makedirs(output_dir, exist_ok=True)

        # Penamaan non-destruktif menggunakan timestamp
        timestamp_filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"weather_raw_{timestamp_filename}.csv"
        output_file = os.path.join(output_dir, file_name)

        # Simpan file CSV raw
        df.to_csv(output_file, index=False)

        print("\n" + "=" * 50)
        print("=== PENGAMBILAN DAN PENYIMPANAN DATA BERHASIL ===")
        print("=" * 50)
        print(f"Lokasi Penyimpanan : {output_file}")
        print(f"Total Baris Data   : {len(df)} baris")
        print("\nPreview 5 Baris Pertama Data Mentah (Raw Data):")
        print(df.head())
        print("=" * 50 + "\n")

    except requests.exceptions.RequestException as req_err:
        print(f"[ERROR] Masalah koneksi/HTTP request: {req_err}")
        sys.exit(1)
    except Exception as err:
        print(f"[ERROR] Terjadi kesalahan tak terduga: {err}")
        sys.exit(1)


if __name__ == "__main__":
    fetch_weather_data()