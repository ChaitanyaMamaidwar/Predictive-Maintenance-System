import os

import joblib

from config import MODEL_PATH


def _clip(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def _heuristic_probability(features):
    """Fallback risk estimate when model file is missing/corrupted."""
    temperature, vibration, pressure, humidity = [float(v) for v in features]

    # Normalize to broad operating ranges.
    temp_score = _clip((temperature - 35.0) / 55.0)
    vib_score = _clip((vibration - 2.5) / 7.5)
    pressure_score = _clip((pressure - 90.0) / 110.0)
    humidity_score = _clip((humidity - 60.0) / 40.0)

    return round(
        (0.35 * temp_score)
        + (0.30 * vib_score)
        + (0.25 * pressure_score)
        + (0.10 * humidity_score),
        4,
    )


def predict(features):
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) == 0:
        return _heuristic_probability(features)

    try:
        model = joblib.load(MODEL_PATH)
        probabilities = model.predict_proba([features])[0]
        classes = list(model.classes_)

        if 1 in classes:
            return float(probabilities[classes.index(1)])

        # One-class model fallback.
        return _heuristic_probability(features)
    except Exception:
        return _heuristic_probability(features)
