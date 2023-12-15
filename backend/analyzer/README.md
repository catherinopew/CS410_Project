# Analyzer Submodule Documentation

## Overview
The Analyzer submodule plays a pivotal role in managing sentiment analysis for Amazon product reviews. This submodule is designed to handle various tasks, including loading machine learning models, retrieving messages containing product reviews from the RabbitMQ channel, transforming reviews into a suitable format, forwarding reviews to the respective models, and aggregating the results of sentiment analysis. The final step involves storing the sentiment analysis results in a PostgreSQL database for further reference and analysis.

## Functionality

1. **Loading Models**: The submodule loads pre-trained models into memory, ensuring they are ready for making predictions.

2. **Prediction Generation**: The submodule accepts messages from a RabbitMQ queue, extracting relevant data, and preparing it for model input. It utilizes the loaded models to generate predictions for the provided data. Then it structures the prediction results in a standardized format for storage and further analysis.

3. **RabbitMQ Integration**: The sunmodule listens for incoming messages on specified RabbitMQ queues and extracts relevant information from the received messages for further analysis.

4. **PostgreSQL Database Interaction**: The submoduke establishes connections to the PostgreSQL database for saving the prediction results, along with any relevant metadata, in a structured format within the database.

## Usage

1. **Initialization**: Initialize the Analyzer submodule by loading the required models and configuring the necessary settings.

2. **RabbitMQ Integration**: Connect to the specified RabbitMQ queues to start listening for incoming messages.

3. **Message Processing**: Upon receiving messages, extract relevant data and pass it to the loaded models for prediction.

4. **Prediction Generation**: Utilize the models to generate predictions based on the received data.

5. **Database Interaction**: Store the results of the analyses in the PostgreSQL database, ensuring data integrity and reliability.

6. **Error Handling**: Implement appropriate error-handling mechanisms to address issues such as model loading failures, message parsing errors, or database connection problems.

## Configuration

The `run_analyzer.py` code features a configurable section where users can connect new machine learning models to the system. \
The relevant code snippet is as follows:

```python
from analyzer.bert_clf.analyzer import get_bert_clf_score
from analyzer.siebert_clf.analyzer import get_siebert_clf_score
from analyzer.lr_clf.analyzer import get_lr_clf_score

UIDs = ('as99', 'romanov2', 'bui5', 'jlo10', 'vdara2')
sa_funcs = (get_bert_clf_score, get_siebert_clf_score, get_lr_clf_score, None, None)
```

## Structure
```bash
.
├── bert_clf
│   ├── dataset
│   └── fine_tuned_bert
├── distilbert_clf
├── lr_clf
│   └── model
├── siebert_clf
│   └── model
└── tests
```

## Files
**analyzer.py** \
this file is located within the folder of the corresponding trained model. This standardized structure ensures ease of access and organization.
It contain a convenient interface for obtaining predictions from the associated trained model.

**model.file** \
it contains soft link to the actual model file

**run_analyzer.py** \
it functions as the main executable responsible for reading reviews from RabbitMQ, obtaining predictions, and subsequently adding the results to a PostgreSQL database.
