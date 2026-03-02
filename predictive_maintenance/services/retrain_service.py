import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from config import MODEL_PATH
from services.data_service import get_training_data
import os

def retrain_model():
    data = get_training_data()

    if len(data) < 20:
        return "Not enough data to train."

    df = pd.DataFrame(data, columns=[
        "temperature", "vibration", "pressure", "humidity", "label"
    ])

    X = df[["temperature", "vibration", "pressure", "humidity"]]
    y = df["label"]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return "Model retrained successfully."