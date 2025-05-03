import pandas as pd
import numpy as np
import os

DATA_FILE = 'merged_rain_flood.csv'
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Load merged data
def load_data():
    path = os.path.join(DATA_DIR, DATA_FILE)
    df = pd.read_csv(path)
    print(f"Loaded merged data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# Feature engineering: rolling rainfall, categorical encoding
def engineer_features(df):
    # Sort for rolling calculations
    df = df.sort_values(['District', 'Year', 'Month']).reset_index(drop=True)
    # Rolling rainfall features (previous 2, 3, 6, 12 months)
    for window in [2, 3, 6, 12]:
        df[f'Rainfall_Last_{window}m'] = (
            df.groupby('District')['MonthlyTotal']
              .shift(1)  # exclude current month
              .rolling(window=window, min_periods=1)
              .sum()
              .reset_index(level=0, drop=True)
        )
    # Calculate rainfall anomaly: current month's rainfall minus long-term average for that district and month
    df['Rainfall_Anomaly'] = 0.0
    # Compute long-term monthly average for each district
    monthly_avg = (
        df.groupby(['Station', 'Year'])['MonthlyTotal'].mean().groupby(level=0).mean()
    )
    for station in df['Station'].unique():
        for month in range(1, 13):
            mask = (df['Station'] == station) & (df['Year'] >= 1948) & (df['Year'] <= 2014)
            month_mask = mask & (df[str(month)].notnull())
            avg = df.loc[month_mask, 'MonthlyTotal'].mean()
            df.loc[(df['Station'] == station) & (df[str(month)].notnull()), 'Rainfall_Anomaly'] = (
                df.loc[(df['Station'] == station) & (df[str(month)].notnull()), 'MonthlyTotal'] - avg
            )
    # Month as categorical (one-hot) with clear names
    month_dummies = pd.get_dummies(df['Month'], prefix='Month')
    # District as categorical (one-hot) with clear names
    district_dummies = pd.get_dummies(df['District'], prefix='District')
    # Concatenate and drop originals
    df = pd.concat([df, month_dummies, district_dummies], axis=1)
    df = df.drop(['Month', 'District'], axis=1)
    # Drop rows with missing rainfall (if any)
    df = df.dropna(subset=['MonthlyTotal'])
    return df

if __name__ == '__main__':
    print("--- Feature Engineering ---")
    df = load_data()
    df_feat = engineer_features(df)
    out_path = os.path.join(DATA_DIR, 'processed_flood_data.csv')
    df_feat.to_csv(out_path, index=False)
    print(f"Processed data saved as {out_path}")
    print("Columns in processed data:", df_feat.columns.tolist())
    print("\nSample:")
    print(df_feat.head()) 