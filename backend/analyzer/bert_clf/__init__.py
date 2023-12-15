import os
import torch

from transformers import BertTokenizer, BertForSequenceClassification


model_dir = os.path.join(os.path.dirname(__file__), 'fine_tuned_bert')

loaded_model = BertForSequenceClassification.from_pretrained(model_dir)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

device = torch.device("cpu")
