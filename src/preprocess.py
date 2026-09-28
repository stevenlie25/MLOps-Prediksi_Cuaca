"""
Data Preprocessing Script for Weather Data.
Processes the latest raw CSV from data/raw/ and exports clean data to data/processed/.
"""

import os
import glob
import sys
import pandas as pd


def get_latest_raw_file(raw_dir: str) -> str:
    """Find the most recently created CSV file in the raw directory."""
    list_of_files = glob.glob(os.path.join(raw_dir, "weather_raw_*.csv"))
    if not list_of_files:
        raise FileNotFoundError("Tidak ditemukan file raw di folder data/raw/")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def preprocess_data() -> None:
    """Clean raw weather data and save processed version."""
    raw_dir = os.path.join("data", "raw")
    processed_dir = os.path.join("data", "processed")

    try:
        raw_file_path = get_latest_raw_file(raw_dir)
        print(f"[INFO] Memproses data dari file: {raw_file_path}")

        df = pd.read_csv(raw_file_path)

        # 1. Konversi kolom time ke datetime format
        df["time"] = pd.to_datetime(df["time"])

        # 2. Penanganan Missing Values (Imputasi/Interpolasi untuk data runtutan waktu)
        if df.isnull().sum().sum() > 0:
            print("[INFO] Ditemukan missing values, melakukan interpolasi...")
            df = df.interpolate(method="linear").bfill().ffill()

        # 3. Penanganan Duplikasi
        initial_count = len(df)
        df = df.drop_duplicates(subset=["time"])
        print(f"[INFO] Menghapus {initial_count - len(df)} baris duplikat.")

        # 4. Pengurutan data berdasarkan waktu
        df = df.sort_values("time").reset_index(drop=True)

        # Buat direktori data/processed
        os.makedirs(processed_dir, exist_ok=True)

        # Simpan data hasil preprocessing
        output_file = os.path.join(processed_dir, "weather_processed.csv")
        df.to_csv(output_file, index=False)

        print("\n" + "=" * 50)
        print("=== PRAPEMROSESAN DATA BERHASIL ===")
        print("=" * 50)
        print(f"File Terproses : {output_file}")
        print(f"Total Baris    : {len(df)} baris")
        print("\nPreview 5 Baris Pertama Data Bersih:")
        print(df.head())
        print("=" * 50 + "\n")

    except Exception as e:
        print(f"[ERROR] Gagal melakukan preprocessing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    preprocess_data()