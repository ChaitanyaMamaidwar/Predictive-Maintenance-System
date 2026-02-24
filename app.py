from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load("model/predictive_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    temp = float(request.form["temperature"])
    vib = float(request.form["vibration"])
    pres = float(request.form["pressure"])

    prediction = model.predict([[temp, vib, pres]])

    if prediction[0] == 1:
        result = "Machine will FAIL soon"
    else:
        result = "Machine is SAFE"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)