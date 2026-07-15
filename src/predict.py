import pandas as pd
import joblib


# Load dataset
df = pd.read_csv("dataset/HDI.csv")


# Load model and encoder once
try:
    model = joblib.load("model/hdi_model.pkl")
    encoder = joblib.load("model/country_encoder.pkl")
    print("Model Loaded Successfully")

except Exception as e:
    print("Model Loading Error:", e)
    model = None
    encoder = None



def predict_country(country):

    if model is None or encoder is None:
        return None


    row = df[df["Country"] == country]


    if row.empty:
        return None


    country_code = encoder.transform([country])[0]


    X = pd.DataFrame({

        "Country": [country_code],

        "Life Expectancy": [
            row.iloc[0]["Life Expectancy"]
        ],

        "Expected Years of Schooling": [
            row.iloc[0]["Expected Years of Schooling"]
        ],

        "Mean Years of Schooling": [
            row.iloc[0]["Mean Years of Schooling"]
        ],

        "GNI per Capita": [
            row.iloc[0]["GNI per Capita"]
        ],

        "Internet Users": [
            row.iloc[0]["Internet Users"]
        ],

        "Population": [
            row.iloc[0]["Population"]
        ],

        "Employment Rate": [
            row.iloc[0]["Employment Rate"]
        ],

        "Health Expenditure": [
            row.iloc[0]["Health Expenditure"]
        ]

    })


    prediction = model.predict(X)[0]


    return {

        "country": country,

        "prediction": round(float(prediction),3),

        "life": row.iloc[0]["Life Expectancy"],

        "expected": row.iloc[0]["Expected Years of Schooling"],

        "mean": row.iloc[0]["Mean Years of Schooling"],

        "gni": row.iloc[0]["GNI per Capita"],

        "internet": row.iloc[0]["Internet Users"],

        "population": row.iloc[0]["Population"],

        "employment": row.iloc[0]["Employment Rate"],

        "health": row.iloc[0]["Health Expenditure"]

    }