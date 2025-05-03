import requests
import h5py
import pandas as pd
import os
from datetime import datetime, timedelta
from io import BytesIO

# User must set their NASA Earthdata token here
EARTHDATA_TOKEN = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImFscGhhNzQ3OCIsImV4cCI6MTc1MTQzODU3NiwiaWF0IjoxNzQ2MjU0NTc2LCJpc3MiOiJodHRwczovL3Vycy5lYXJ0aGRhdGEubmFzYS5nb3YiLCJpZGVudGl0eV9wcm92aWRlciI6ImVkbF9vcHMiLCJhY3IiOiJlZGwiLCJhc3N1cmFuY2VfbGV2ZWwiOjN9.sHpjzVjIEcL4GXUxmcNzsiR_fs1S_4dTikAXQjwvbWW7PNEPW3wmhYgwtRVJLCQRCRumvAePGOttzC5qKHOkQ4wQyEhH84rkTIrvZImtOxRoesQYVdOraoz-QG00tTm85k48AWlyujDl4zP1gRXchOb5kQXQee4X63_DEuI-SkejOZt8nutUyFDs0-Hs8AdfDsaWpKK_BF298IN3uN10Yw3nSn0qKj0h_CERzNUb0JvVD50-3L4N24Tt09Zkk6grgBbRngq-EuLLa53aIhHgqAtFEudZgL6cz9x6iF0diz-lu-3nP5kVEtW6vaAU5WVFq2_q09Ejv3Dw9soJu3ZBRw"

# Bangladesh bounding box (approx)
LAT_MIN, LAT_MAX = 20.5, 26.7
LON_MIN, LON_MAX = 88.0, 92.7

# IMERG Late Run (Final) product URL pattern (change date as needed)
IMERG_BASE_URL = "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDL.06/"

def get_latest_imerg_url():
    for delta in range(0, 7):
        day = datetime.utcnow() - timedelta(days=delta)
        date_str = day.strftime("%Y/%m/%d")
        file_date_str = day.strftime("%Y%m%d")
        filename = f"3B-DAY-L.MS.MRG.3IMERG.{file_date_str}-S000000-E235959.V06.nc4"
        file_url = f"{IMERG_BASE_URL}{date_str}/{filename}"
        headers = {"Authorization": f"Bearer {EARTHDATA_TOKEN}"}
        try:
            resp = requests.head(file_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                return file_url, day
        except Exception:
            continue
    return None, None

def fetch_imerg_bangladesh(csv_path=None):
    if EARTHDATA_TOKEN == "<PASTE_YOUR_TOKEN_HERE>":
        print("Please set your NASA Earthdata token in the script.")
        return False
    file_url, file_day = get_latest_imerg_url()
    if not file_url:
        print("Could not find a recent IMERG file to download.")
        return False
    print(f"Downloading: {file_url}")
    headers = {"Authorization": f"Bearer {EARTHDATA_TOKEN}"}
    try:
        resp = requests.get(file_url, headers=headers, timeout=60)
        resp.raise_for_status()
        print("Download successful. Extracting data...")
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
    # Read NetCDF4 file from memory
    with h5py.File(BytesIO(resp.content), 'r') as f:
        lat = f['lat'][:]
        lon = f['lon'][:]
        precip = f['precipitationCal'][:]
        # Find indices for Bangladesh
        lat_idx = (lat >= LAT_MIN) & (lat <= LAT_MAX)
        lon_idx = (lon >= LON_MIN) & (lon <= LON_MAX)
        # Meshgrid for all points in Bangladesh
        lats, lons = lat[lat_idx], lon[lon_idx]
        precip_bd = precip[0, lat_idx, :][:, lon_idx]  # [time, lat, lon] -> [lat, lon]
        # Flatten to DataFrame
        data = []
        for i, la in enumerate(lats):
            for j, lo in enumerate(lons):
                data.append({
                    'date': file_day.strftime('%Y-%m-%d'),
                    'lat': float(la),
                    'lon': float(lo),
                    'precip_mm': float(precip_bd[i, j])
                })
        df = pd.DataFrame(data)
        if csv_path is None:
            csv_path = os.path.join(os.path.dirname(__file__), 'nasa_imerg_latest.csv')
        df.to_csv(csv_path, index=False)
        print(f"Saved to {csv_path}")
        return True

if __name__ == "__main__":
    fetch_imerg_bangladesh() 