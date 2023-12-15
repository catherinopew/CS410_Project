import os
from joblib import load


model_path = os.path.join(os.path.dirname(__file__), 'model/trained_logistic_regression.joblib')

pipeline = load(model_path)
loaded_vectorizer = pipeline.named_steps['vectorizer']
loaded_model = pipeline.named_steps['logistic_regression']
