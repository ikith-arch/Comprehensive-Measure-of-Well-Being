import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder

os.makedirs("model", exist_ok=True)

# Load Dataset
df = pd.read_csv("dataset/HDI.csv")

print("Dataset Loaded Successfully")
print(df.head())

# Check Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Fill Missing Values
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].mean())

# Encode Country
encoder = LabelEncoder()
df["Country"] = encoder.fit_transform(df["Country"])

# Save Encoder
joblib.dump(encoder, "model/country_encoder.pkl")

# Save Clean Dataset
df.to_csv("dataset/cleaned_HDI.csv", index=False)

print("\nClean Dataset Saved Successfully!")
print(df.head())