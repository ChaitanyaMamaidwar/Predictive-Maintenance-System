import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("data/machine_data.csv")

# Split features and target
X = data[['temperature', 'vibration', 'pressure']]
y = data['failure']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "model/predictive_model.pkl")

print("Model trained and saved successfully.")