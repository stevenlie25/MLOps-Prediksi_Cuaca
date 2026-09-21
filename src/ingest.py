import os
import sys
import requests
import pandas as pd
from datetime import datetime

def fetch_weather_data():
    # 1. Parameter Endpoint Open-Meteo API (Lokasi: Kota Malang)
    URL = "https://api.open-meteo.com/v1/forecast"
    PARAMS = {
        "latitude": -7.9839,       # Latitude Malang
        "longitude": 112.6214,     # Longitude Malang
        "hourly": [
            "temperature_2m", 
            "relative_humidity_2m", 
            "surface_pressure", 
            "wind_speed_10m", 
            "precipitation"
        ],
        "timezone": "Asia/Jakarta",
        "past_days": 2             # Mengambil data 2 hari terakhir untuk time-series
    }

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mengirim request ke Open-Meteo API...")
    
    try:
        # 2. Kirim Request HTTP GET
        response = requests.get(URL, params=PARAMS, timeout=10)
        
        # Cetak Status Code untuk Verifikasi
        print(f"HTTP Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # 3. Ekstraksi Data ke Pandas DataFrame
            df = pd.DataFrame(data["hourly"])
            df["time"] = pd.to_datetime(df["time"])
            
            # 4. Pastikan Direktori data/raw/ Ada
            output_dir = os.path.join("data", "raw")
            os.makedirs(output_dir, exist_ok=True)
            
            # 5. Simpan ke File CSV
            output_file = os.path.join(output_dir, "weather_raw.csv")
            df.to_csv(output_file, index=False)
            
            print("\n" + "="*50)
            print("=== PENGAMBILAN DAN PENYIMPANAN DATA BERHASIL ===")
            print("="*50)
            print(f"Lokasi Penyimpanan : {output_file}")
            print(f"Total Baris Data   : {len(df)} baris")
            print("\nPreview 5 Baris Pertama Data Mentah (Raw Data):")
            print(df.head())
            print("="*50 + "\n")
            
        else:
            print(f"[ERROR] Gagal mengambil data. HTTP Status Code: {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat menjalankan ingestion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_weather_data()