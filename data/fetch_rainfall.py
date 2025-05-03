import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os

def fetch_rainfall_data(csv_path=None):
    url = "http://www.hydrology.bwdb.gov.bd/includes/get_rainfall_datatable.php"
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), 'rainfall_latest.csv')
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
        df = pd.read_html(StringIO(str(table)))[0]
        df.to_csv(csv_path, index=False)
        print(f"Saved to {csv_path}")
        return True
    except Exception as e:
        print(f"Error parsing or saving table: {e}")
        return False

if __name__ == "__main__":
    fetch_rainfall_data() 