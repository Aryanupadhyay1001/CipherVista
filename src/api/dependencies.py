import joblib

isolation_model = joblib.load("models/isolation_forest.pkl")
classifier_model = joblib.load("models/random_forest.pkl")
scaler = joblib.load("models/scaler.pkl")