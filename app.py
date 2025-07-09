from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib

app = Flask(__name__)

# Features to use
features = ["GrLivArea", "BedroomAbvGr", "FullBath", "GarageArea", "YearBuilt", "OverallQual"]

# Load and prepare dataset
df = pd.read_csv("train.csv")
df = df[features + ["SalePrice"]].dropna()

X = df[features]
y = df["SalePrice"]

# Scale & train
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LinearRegression()
model.fit(X_scaled, y)

# Save models
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(features, "features.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        features = joblib.load("features.pkl")
        input_df = pd.DataFrame([{f: float(data[f]) for f in features}])
        
        scaler = joblib.load("scaler.pkl")
        model = joblib.load("model.pkl")

        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]

        return jsonify({"price": round(prediction, 2)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
