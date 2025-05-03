import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

def fetch_latest_data(csv_path="waterlevel_latest.csv", river_id=""):
    url = "http://www.hydrology.bwdb.gov.bd/includes/water_level_auto_datatable.php"
    params = {"river_id": river_id, "dist_id": ""}

    try:
        response = requests.get(url, params=params, timeout=30)
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
        df = pd.read_html(StringIO(str(table)))[0]
    except Exception as e:
        print(f"Error parsing table: {e}")
        return False

    try:
        df.to_csv(csv_path, index=False)
        print(f"Saved to {csv_path}")
        return True
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return False

if __name__ == "__main__":
    success = fetch_latest_data()
    if success:
        print("Data fetch and save successful.")
    else:
        print("Data fetch failed.")
