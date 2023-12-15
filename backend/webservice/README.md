# RESTful Web Service

## Overview

The RESTful web service allows clients to interact with the system by providing a URL to an Amazon product page. The service forwards input data to server apps and, once processing is completed, returns sentiment for each product review. It provides functionalities to send requests and retrieve responses through two API functions: `send_request` and `get_response`. These functions facilitate communication between clients and the service, enabling the exchange of data.

## Base URL

The base URL for accessing the API is `https://34.239.197.4:8080`.

## Authentication

No authentication is required.

---

## `send_request` example

### Endpoint

```
POST http://34.239.197.4:8080/send_request
```

### Description

This endpoint allows clients to send requests to the service.

### Request

- **Method**: POST
- **Headers**:
  - `Content-Type: application/json`
- **Body**:

```json
{
  "client_id": "my_client_id",
  "url": "amazon_product_url",
  "reviews": []
}
```

### Response

Status Codes:

**200 OK**: Request successfully sent.

**400 ERROR**: Invalid JSON data / Missing required keys.

**500 Internal Server Error**: An error occurred on the server.

```json
{
    "message": {
        "task_id": "2939f5f62dfbe9c106857ab97b46a918"
    },
    "status": "ok"
}
```

---

## `get_response` POST example

### Endpoint

POST http://34.239.197.4:8080/get_response


## Request

- **Method**: POST
- **Headers**:
  - `Content-Type: application/json`
- **Body** (JSON):

```json
{
  "task_id": "2939f5f62dfbe9c106857ab97b46a918",
  "client_id": "my_client"
}
```

###Response

Status Codes:

**200 OK**: In progress

**400 ERROR**: Task not found / Reviews not found

```{json}
{
  "status": "ok",
  "message": {
    "task_id": "2939f5f62dfbe9c106857ab97b46a918",
    "reviews": {
      "0002600306947ca04b180349099c69ef": {
        "content": "content",
        "sentiment": {
          "as99": 1,
          "bui5": 1,
          "jlo10": null,
          "romanov2": 1,
          "vdara2": null
        }
      },
      // ... (other review entries)
    }
  }
}

```
