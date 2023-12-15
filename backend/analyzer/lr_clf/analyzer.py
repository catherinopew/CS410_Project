from . import loaded_vectorizer, loaded_model


def get_lr_clf_score(text_list):
    sentiments = []

    for text in text_list:
        text_features = loaded_vectorizer.transform([text])

        prediction = loaded_model.predict_proba(text_features)
        max_index = prediction.argmax(axis=1)[0]
        if max_index == 0:
            score = -1
        elif max_index == 1:
            score = 0
        else:
            score = 1
        sentiments.append(score)

    return sentiments
