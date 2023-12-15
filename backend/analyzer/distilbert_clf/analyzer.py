from . import tokenizer, model

def get_distilbert_clf_score(text):
    neutral_threshold = 0.2
    sentiments = []
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits

    for logit in logits:
        if logit[1] - logit[0] > neutral_threshold:
            sentiments.append(1)
        elif logit[0] - logit[1] > neutral_threshold:
            sentiments.append(-1)
        else:
            sentiments.append(0)

    return sentiments