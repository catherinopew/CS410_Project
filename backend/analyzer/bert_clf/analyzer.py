import torch
import torch.nn.functional as F

from . import loaded_model, tokenizer, device

def get_probs(text, tokenizer=tokenizer, device=device):
    loaded_model.eval()

    with torch.no_grad():
        tokenized_sentence = tokenizer(text, truncation=True, padding='max_length', max_length=256, return_tensors='pt')
        input_ids = tokenized_sentence["input_ids"].to(device)
        attention_mask = tokenized_sentence["attention_mask"].to(device)

        outputs = loaded_model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)
    
    return probs

def prob_to_class(probs):
    threshold = 0.5

    probs_diff = probs[:, 1] - probs[:, 0]

    v = torch.zeros_like(probs_diff, dtype=torch.int)
    v[probs_diff > threshold] = 1
    v[probs_diff < -threshold] = -1
    
    return v

def get_bert_clf_score(text):
    return prob_to_class(get_probs(text)).tolist()