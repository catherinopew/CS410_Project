from . import fine_tuned_pipeline


def get_siebert_clf_score(inputs):
    """
    Analyze the sentiment of the input text.
    :param inputs: a tuple of strings
    :return: a list of integers, each integer is either -1, 1, or 0
    """
    if fine_tuned_pipeline is None:
        raise Exception("Pipeline not initialized.")

    if not isinstance(inputs, tuple):
        raise TypeError("Input must be a tuple.")

    if len(inputs) == 0:
        return []

    results = []
    for i in range(len(inputs)):

        if type(inputs[i]) is not str:
            raise TypeError("Input must be a list of strings.")

        if len(inputs[i]) == 0:
            results.append(0)
            continue

        output = fine_tuned_pipeline(inputs[i])
        negative_score, positive_score = output[0][0]['score'], output[0][1]['score']
        pred_label = 1 if positive_score > negative_score else -1
        results.append(pred_label)

    return results


def init():
    pass
