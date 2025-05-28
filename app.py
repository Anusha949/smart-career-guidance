from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

model = pickle.load(open("model/model.pkl", "rb"))
le_interests = pickle.load(open("model/le_interests.pkl", "rb"))
le_career = pickle.load(open("model/le_career.pkl", "rb"))
mlb_skills = pickle.load(open("model/mlb_skills.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        score10 = float(data["score10"])
        score12 = float(data["score12"])
        ugscore = float(data["ugscore"])
        interests = data["interests"]
        skills = data["skills"]

        encoded_interest = le_interests.transform([interests])[0]
        skills_encoded = mlb_skills.transform([skills])
        input_features = np.concatenate([[score10, score12, ugscore, encoded_interest], skills_encoded[0]])
        prediction = model.predict([input_features])[0]
        career = le_career.inverse_transform([prediction])[0]

        return jsonify({"career": career})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
