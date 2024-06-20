from flask import Flask, request, render_template
import pandas as pd
import json
import joblib

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load("tac_predictor_model.pkl")


# Load the JSONL file into a DataFrame
def jsonl_to_dataframe(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    df = pd.DataFrame(data)
    return df


# Path to the JSONL file
file_path = "DeviceDatabase_first_500.jsonl"

# Load the DataFrame
df = jsonl_to_dataframe(file_path)


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

        # Get the prediction from the model
        prediction = model.predict(features)

        # Lookup the device in the DataFrame
        device_info = df[df["tac"] == tac]

        # If device_info is empty, handle it
        if device_info.empty:
            return render_template("index.html", error="Device not found.")

        device_info = device_info.iloc[
            0
        ].to_dict()  # Convert the first matching row to a dictionary

        return render_template(
            "index.html", prediction=prediction, device_info=device_info
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
