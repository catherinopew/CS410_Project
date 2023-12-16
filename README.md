# CS410 Course Project : AMZSentiment

## Overview

[AMZSentiment Installation and Usage Tutorial](https://www.youtube.com/watch?v=JfcbqbA6XCw)

[Code Overview](https://www.youtube.com/watch?v=QVRPHDk0c8g) - Chapters for each of the code sections can be found in the video description.

AMZSentiment, a Chrome extension seamlessly integrated with Amazon product pages, offers real-time sentiment analysis
from multiple models. With an intuitive interface displaying sentiment indicators, users quickly grasp overall emotional
tones—positive, negative, or neutral. Its unique feature allows granular analysis for deeper insights and personalized
opinions, synthesizing information from various ML models. AMZSentiment not only provides a comprehensive view of
sentiments but also empowers users to make informed decisions based on nuanced emotional contexts within Amazon product
reviews.

![extension example](/docs/imgs/extension.png)

## Schema

![project schema](/docs/imgs/schema.png)

## Source Code Documentation

1. [Server](/backend/README.md) \
   1.1 [Webservice](backend/webservice/README.md) \
   1.2 [Analyzer](backend/analyzer/README.md) \
   1.3 [Scraper](https://github.com/alyosharomanov/amazon-review-api/blob/148d911bb97bca1cda8fb6a44645eab7aad09535/README.md)
2. [Extension](frontend/extension/README.md)

## Team Members

**Team Name:** Bag-of-Cats

**Team Members:**

- Catherine Bui (@bui5)
- Aleksandr Stepenko (@as99)
- Alyosha Romanov (@romanov2)
- ~~Josephine Lo (@jlo10)~~
    * Josephine was assigned the tasks of creating her own model to perform sentiment analysis and to work on the
      parser. However, no work was completed. Therefore, she has 0% contribution and is excluded from the team.
- ~~Vikram Dara (@vdara2)~~
    * Vikram was also assigned the tasks of creating his own model to perform sentiment analysis and to work on the
      parser. However, no work was completed. Therefore, he has 0% contribution and is excluded from the team.

Catherine, Aleksandr, and Alyosha all contributed equally to the project and worked on multiple aspects of it.

## Tech Stack

Client (Chrome Plug-in):

    Language: JavaScript, HTML/CSS
    Framework: Chrome Extension API

Server (Flask-based RESTful Web Service):

	Language: Python
    Framework: Flask
    Database: PostgreSQL
    Message Queue: RabbitMQ
    ML Libraries: PyTorch, scikit-learn

## Quick Start

~~You can install the extension from the [Chrome Web Store](https://chromewebstore.google.com/).~~ \
Note: The extension is currently in the review process and is not yet available on the Chrome Web Store. You can still
install it locally by following the steps below.

If you want to run the extension locally, follow the steps below.

1. Clone the repository.
2. In Chrome (or any Chromium-based browser), go to `chrome://extensions/` and enable developer mode.
3. Click on "Load unpacked" and select the `frontend/extension` folder.
4. Navigate to any Amazon product page and click on the extension icon.
5. The extension will redirect you to the review page and display the sentiment analysis results for the product
   reviews.
6. Click on the "Next" button to navigate to the next page of reviews.

You can refer to the [Installation and Usage Tutorial](https://www.youtube.com/watch?v=JfcbqbA6XCw) for more details.

## Details

The extension may display various error.

| Error                                                                          | Explanation                                                    |
|--------------------------------------------------------------------------------|----------------------------------------------------------------|
| Extension cannot be used here. Please open an Amazon (US) product review page. | The extension can only be used on Amazon product review pages. |
| No reviews found on the page.                                                  | The extension cannot find any reviews on the page.             |
| Server is currently not available. Please try again later.                     | The server is temporarily unavailable.                         |

## Project Layout

```bash
$tree . -d                                                           
.
├── backend
│   ├── analyzer
│   │   ├── bert_clf
│   │   │   ├── dataset
│   │   │   └── model
│   │   ├── distilbert_clf
│   │   ├── lr_clf
│   │   │   └── model
│   │   ├── siebert_clf
│   │   │   └── model
│   │   └── tests
│   ├── weblogger
│   ├── webscraper
│   ├── webservice
│   └── webutils
├── docs
└── frontend
    ├── extension
    │   └── Icons
    └── scripts
```

