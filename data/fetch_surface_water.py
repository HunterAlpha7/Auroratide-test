import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os

COASTAL_STATION_IDS = [
    60002, 60040, 60023, 60039, 60001, 60038, 6003, 60034, 60033, 60035, 60031, 60032, 60036, 60037, 60005, 60006, 60007, 60004, 60008, 60025, 60026, 60029, 60024, 60028, 60027, 60030, 60013, 60011, 60012, 6009, 60014, 60010, 60018, 60015, 60016, 60017, 60019, 60020
]

def fetch_surface_water(csv_path=None):
    url = "http://www.hydrology.bwdb.gov.bd/includes/water_level_auto_datatable.php"
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), 'surface_water_latest.csv')
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "example"})
    if table is None:
        print("Error: Could not find the data table on the page.")
        return False
    try:
        df = pd.read_html(StringIO(str(table)), header=[0, 1])[0]
        # Flatten MultiIndex columns
        df.columns = [col[0] if col[0] == col[1] else col[1] for col in df.columns.values]
        # Remove duplicate header rows if present
        if 'Station ID' in df.columns:
            df = df[df['Station ID'] != 'Station ID']
        df.to_csv(csv_path, index=False)
        print(f"Saved to {csv_path}")
        return df
    except Exception as e:
        print(f"Error parsing or saving table: {e}")
        return False

def fetch_coastal_tide(csv_path=None):
    df = fetch_surface_water()
    if isinstance(df, pd.DataFrame):
        if 'Station ID' in df.columns:
            coastal_df = df[df['Station ID'].astype(str).isin([str(sid) for sid in COASTAL_STATION_IDS])]
            if csv_path is None:
                csv_path = os.path.join(os.path.dirname(__file__), 'coastal_tide_latest.csv')
            coastal_df.to_csv(csv_path, index=False)
            print(f"Saved coastal tide data to {csv_path}")
            return True
        else:
            print("'Station ID' column not found after flattening columns.")
    return False

if __name__ == "__main__":
    fetch_surface_water()
    fetch_coastal_tide() 