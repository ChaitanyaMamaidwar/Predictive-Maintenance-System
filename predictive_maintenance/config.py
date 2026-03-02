import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "database", "database.db")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

SECRET_KEY = "super-secret-key"

FAILURE_THRESHOLD = 0.70
HEALTH_ALERT_THRESHOLD = 40