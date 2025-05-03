import pandas as pd
import numpy as np
import os

# Paths to data files (update if needed)
FLOOD_CSV = 'Flood data (2000 - 2025).csv'
RAIN_MONTHLY_CSV = 'rainfall_modified_data_bangladesh_1948_to_2014.csv'
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Load flood event data
def load_flood_data():
    path = os.path.join(DATA_DIR, FLOOD_CSV)
    df = pd.read_csv(path)
    print(f"Flood data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print("Columns:", df.columns.tolist())
    print(df.head())
    return df

# Load rainfall data (monthly totals)
def load_rainfall_data():
    path = os.path.join(DATA_DIR, RAIN_MONTHLY_CSV)
    df = pd.read_csv(path)
    print(f"Rainfall data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print("Columns:", df.columns.tolist())
    print(df.head())
    return df

# Summarize missing data
def summarize_missing(df, name):
    print(f"\nMissing data summary for {name}:")
    print(df.isnull().sum())

# Prepare merged dataset for modeling
def prepare_merged_data(flood_df, rain_df):
    # Extract flood events by district and month
    flood_events = []
    for _, row in flood_df.iterrows():
        # Some events have multiple districts
        if pd.isnull(row['Admin Units']):
            continue
        try:
            import ast
            admin_units = ast.literal_eval(row['Admin Units'])
            for unit in admin_units:
                event = {
                    'Year': row['Start Year'],
                    'Month': row['Start Month'],
                    'District': unit.get('adm2_name', None),
                    'Flood': 1
                }
                flood_events.append(event)
        except Exception as e:
            continue
    flood_events_df = pd.DataFrame(flood_events)
    # Merge with rainfall data
    rain_df['District'] = rain_df['Station']
    merged = pd.merge(rain_df, flood_events_df, how='left', on=['Year', 'Month', 'District'])
    merged['Flood'] = merged['Flood'].fillna(0).astype(int)
    print(f"\nMerged dataset: {merged.shape[0]} rows, {merged.shape[1]} columns")
    print(merged[['Year', 'Month', 'District', 'MonthlyTotal', 'Flood']].head(10))
    merged.to_csv(os.path.join(DATA_DIR, 'merged_rain_flood.csv'), index=False)
    print("\nMerged data saved as merged_rain_flood.csv")
    return merged

if __name__ == '__main__':
    print("--- Loading Data ---")
    flood_df = load_flood_data()
    rain_df = load_rainfall_data()
    summarize_missing(flood_df, 'Flood Data')
    summarize_missing(rain_df, 'Rainfall Data')
    print("\n--- Preparing Merged Dataset ---")
    merged = prepare_merged_data(flood_df, rain_df)
    print("\nDone. Ready for feature engineering and modeling.") 