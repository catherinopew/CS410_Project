# Server: Sentiment Analysis of Amazon Product Reviews Application

## Overview

The **Sentiment Analysis of Amazon Product Reviews** application is designed to analyze and evaluate the sentiments expressed in Amazon product reviews. The application comprises two main components: the client, implemented as a Chrome extension, and the server, which consists of a set of submodules including a RESTful web service and an analyzer.

## Server

The server is responsible for handling the core functionalities of the application, including performing sentiment analysis (provided by multi models), serving the results via a RESTful web service, and others.

### Installation

1. Clone the repository from [GitHub Link](https://github.com/catherinopew/CS410_projectv2.git).
2. Navigate to the `project` directory.
3. Create virtual environment
4. Install dependencies
6. Install rabbitmq
7. Install postgresql

```bash
python3 -n venv venv
. venv/bin/activate

pip install -r requirements.txt

sudo apt -y install rabbitmq-server postgresql
```

### Configuration
Modify the configuration files (config.yaml) to include necessary credentials, database and rabbitmq server connection details, and other settings.

**RabbitMQ Configuration**

- **Host:** localhost
- **Port:** 5672
- **Queue Name:** messages
- **Username:** user
- **Password:** password
- **Connection Attempts:** 3
- **Retry Delay:** 5
- **Socket Timeout:** 5
- **Heartbeat:** 36000

**PostgreSQL Configuration**

- **Host:** localhost
- **Port:** 5432
- **Database:** app_db
- **Username:** user
- **Password:** password
- **Minimum Connections:** 1
- **Maximum Connections:** 5

### Submodules
1. RESTful Web Service
The RESTful web service provides endpoints for communication between the client and the server.
Endpoints:
/send_request: Initiates sentiment analysis for the currently opened Amazon product.
/get_response: Returns the results of sentiment analysis for each product review.

Usage:
```bash
python3 run_ws.py
```

[See more](webservice/README.md)

2. Analyzer
The analyzer submodule is designed to processes reviews and conducts sentiment analysis using machine learning models developed and trained by team members. It consumes messages from the "ws_messages" queue and operates asynchronously alongside the web service.

Usage:
```bash
python3 run_analyzer.py
```

[See more](analyzer/README.md)

### Communication
RabbitMQ is a message broker software that facilitates communication between different software components, providing a reliable and scalable mechanism for the exchange of messages. In our system, RabbitMQ plays a central role, enabling seamless communication between the submodules. For example, webservice and analyzer modules through the designated ws_messages queue.

### Database
All results of server core activities including results of sentiment analysis are written to a PostgreSQL database.

Structure:
Table: results

This table stores information about status of task.
| Column     | Type                    | Nullable |
|------------|-------------------------|----------|
| id         | integer                 | not null |
| client_id  | character varying(32)   | not null | 
| task_id    | character varying(32)   | not null |
| timestamp  | bigint                  | not null |
| url        | character varying(2048) | not null |
| score      | integer                 |          |
| status     | character varying(16)   | not null |

Indexes:

    results_pkey: Primary key on the "id" column.
    client_id_idx: Index on the "client_id" column.
    task_id_idx: Index on the "task_id" column.

Table: 
| Column         | Type                    | Nullable |
|----------------|-------------------------|----------|
| id             | integer                 | not null |
| task_id        | character varying(32)   | not null |
| status         | character varying(255)  | not null |
| review_id      | character varying(32)   | not null |
| content        | text                    |          |
| score_as99     | integer                 |          |
| score_romanov2 | integer                 |          |
| score_bui5     | integer                 |          |
| score_jlo10    | integer                 |          |
| score_vdara2   | integer                 |          |

Indexes:

    reviews_pkey: Primary key on the "id" column.
    task_id_idx: Index on the "task_id" column.
    review_id_idx: Index on the "review_id" column.

There is a foreign key relationship between the "task_id" column in the "results" table and the "task_id" column in the "reviews" table.

### Running the Server Apps
1. Start the RabbitMQ server.
2. Start postgresql daemon.
3. Start the applications
 
```bash
sudo service rabbitmq-server start
sudo service posqtgresql start

sudo service analyzer start

cd proj_folder
gunicorn -w 2 -b 0.0.0.0:8080 run_ws:app --daemon
```

## Files

**pool.py** \
it contains the implementation of a class for interacting with the PostgreSQL database.

**rmq.py** \
it contains the implementation of a class for interacting with RabbitMQ.

**utils.py** \ 
it contains various supplementary functions used across the application.

**setup_db.sh** \
it is a shell script for setting up the PostgreSQL database

**config.yaml** \ 
it is a YAML configuration file used to store settings and parameters for the application. \
It is utilized by both pool.py and rmq.py to configure connections to the PostgreSQL database and RabbitMQ server, respectively.
