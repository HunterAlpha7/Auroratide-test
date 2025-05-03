import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from imblearn.over_sampling import SMOTE

DATA_FILE = 'processed_flood_data.csv'
MODEL_FILE = 'rf_flood_model.joblib'
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Load processed data
def load_data():
    path = os.path.join(DATA_DIR, DATA_FILE)
    df = pd.read_csv(path)
    print(f"Loaded processed data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

if __name__ == '__main__':
    print("--- Model Training ---")
    df = load_data()
    # Features: all except non-numeric and target
    feature_cols = [col for col in df.columns if col not in ['Year', 'District', 'Station', 'Flood'] and df[col].dtype in [np.float64, np.int64]]
    X = df[feature_cols]
    y = df['Flood']
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Class distribution before SMOTE: {np.bincount(y_train)}")
    # Drop rows with NaN in X_train before SMOTE
    nan_mask = ~X_train.isnull().any(axis=1)
    X_train = X_train[nan_mask]
    y_train = y_train[nan_mask]
    print(f"X_train shape after dropping NaNs: {X_train.shape}")
    # Apply SMOTE to balance the classes in the training set
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    print(f"Class distribution after SMOTE: {np.bincount(y_train_res)}")
    # Train Random Forest with class weights
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight='balanced')
    clf.fit(X_train_res, y_train_res)
    # Predict and evaluate
    y_pred = clf.predict(X_test)
    print("\n--- Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred, digits=4))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    # Printing importances
    importances = clf.feature_importances_
    feature_importance_df = pd.DataFrame({'feature': feature_cols, 'importance': importances})
    print(feature_importance_df.sort_values('importance', ascending=False).head(20))
    # Save model
    model_path = os.path.join(DATA_DIR, MODEL_FILE)
    joblib.dump(clf, model_path)
    print(f"\nModel saved as {model_path}") 