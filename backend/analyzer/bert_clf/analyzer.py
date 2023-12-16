import torch
import torch.nn.functional as F

# Importing model-related modules from the same package
from . import loaded_model, tokenizer, device

# Function to get class probabilities for a given text using a loaded BERT model
def get_probs(text, tokenizer=tokenizer, device=device):
    loaded_model.eval()

    # Tokenize the input text and prepare input tensors
    with torch.no_grad():
        tokenized_sentence = tokenizer(text, truncation=True, padding='max_length', max_length=256, return_tensors='pt')
        input_ids = tokenized_sentence["input_ids"].to(device)
        attention_mask = tokenized_sentence["attention_mask"].to(device)

        # Forward pass through the loaded BERT model
        outputs = loaded_model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)
    
    return probs

# Function to convert class probabilities to predicted classes based on a threshold
def prob_to_class(probs):
    threshold = 0.5

    # Calculate the difference between class probabilities
    probs_diff = probs[:, 1] - probs[:, 0]

    # Create a tensor of zeros with the same shape as probs_diff
    v = torch.zeros_like(probs_diff, dtype=torch.int)

    # Set values in v based on the threshold
    v[probs_diff > threshold] = 1
    v[probs_diff < -threshold] = -1
    
    return v

# Function to get binary classification score using BERT model
def get_bert_clf_score(text):
    return prob_to_class(get_probs(text)).tolist()
