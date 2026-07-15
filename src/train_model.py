import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ============================================
# Load Clean Dataset
# ============================================

df = pd.read_csv("dataset/cleaned_HDI.csv")

print("=" * 60)
print("CLEAN DATASET LOADED")
print("=" * 60)

print(df.head())

# ============================================
# Features and Target
# ============================================

X = df.drop("HDI", axis=1)

y = df["HDI"]

print("\nFeatures Shape :", X.shape)
print("Target Shape :", y.shape)

# ============================================
# Train Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples :", len(X_test))

# ============================================
# Model Training
# ============================================

model = LinearRegression()

model.fit(X_train, y_train)

print("\nModel Training Completed Successfully")

# ============================================
# Prediction
# ============================================

y_pred = model.predict(X_test)

# ============================================
# Evaluation
# ============================================

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)

r2 = r2_score(y_test, y_pred)

print("\n================ MODEL PERFORMANCE ================")

print(f"MAE  : {mae:.6f}")

print(f"MSE  : {mse:.6f}")

print(f"RMSE : {rmse:.6f}")

print(f"R2 Score : {r2:.6f}")

# ============================================
# Compare Predictions
# ============================================

comparison = pd.DataFrame({

    "Actual HDI": y_test.values,

    "Predicted HDI": y_pred

})

print("\nPrediction Comparison")

print(comparison.head(15))

# ============================================
# Save Model
# ============================================

os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/hdi_model.pkl")

print("\nModel Saved Successfully")

print("Location : model/hdi_model.pkl")

print("=" * 60)