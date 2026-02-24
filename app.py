from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    temperature = float(request.form["temperature"])
    vibration = float(request.form["vibration"])
    pressure = float(request.form["pressure"])

    # Temporary prediction logic
    if temperature > 80 or vibration > 50:
        result = "Machine will FAIL soon"
    else:
        result = "Machine is SAFE"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)