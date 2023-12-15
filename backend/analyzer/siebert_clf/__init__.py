import os
from transformers import pipeline

model_dir = os.path.join(os.path.dirname(__file__), 'model')
fine_tuned_pipeline = pipeline("sentiment-analysis", model=model_dir, return_all_scores=True)
