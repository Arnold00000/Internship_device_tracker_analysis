from flask import Flask, request, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load("tac_predictor_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        tac = request.form["tac"]
        reportingBodyId = int(tac[:2])
        manufacturerModelId = int(tac[2:])
        features = pd.DataFrame(
            [[reportingBodyId, manufacturerModelId]],
            columns=["reportingBodyId", "manufacturerModelId"],
        )
        prediction = model.predict(features)
        return render_template("index.html", prediction=prediction)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
