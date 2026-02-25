import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Load dataset
data = pd.read_csv("../data/machine_data.csv")

X = data[['temperature', 'vibration', 'pressure']]
y = data['failure']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model properly
model_path = "../models/model.pkl"

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully.")