def calculate_health_score(probability):
    return round(100 - (probability * 100), 2)