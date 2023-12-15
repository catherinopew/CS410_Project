document.addEventListener('DOMContentLoaded', function () {

    const ldsRing = document.querySelector('.lds-ring');
    const loadMsg = document.querySelector('.loading-msg');

    function displayError(message, consoleMessage) {
        console.log(consoleMessage);
        ldsRing.style.display = 'none';
        loadMsg.style.display = 'none';
        displayErrorMessage(message);
    }

    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        let activeTab = tabs[0];
        let url = activeTab.url;

        if (isProductPage(url)) {
            let newUrl = url.replace("/dp/", "/product-reviews/");
            chrome.tabs.update(activeTab.id, {url: newUrl});
        } else if (!isReviewPage(url)) {
            displayError('Extension cannot be used here. Please open an Amazon (US) product review page.', 'not a review page');
        } else {
            initExtension(url);
        }
    });

    chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
        if (changeInfo.status === 'complete' && tab.active) {
            initExtension(tab.url);
        }
    });

    function getCurrentTabUrl(callback) {
        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
            let activeTab = tabs[0];
            let url = activeTab.url;

            if (isProductPage(url)) {
                let newUrl = url.replace("/dp/", "/product-reviews/");
                chrome.tabs.update(activeTab.id, {url: newUrl});
            } else {
                callback(url);
            }
        });
    }

    function createButton() {
        const nextPageButton = document.querySelector('.button-1');

        if (!nextPageButton) {
            const button = document.createElement('button');
            button.className = 'button-1';
            button.setAttribute('role', 'button');
            button.textContent = 'Next Page';
            const body = document.body;
            body.appendChild(button);
        } else {
            nextPageButton.disabled = false;
        }
    }

    function initExtension(currentUrl) {
        getCurrentTabUrl(function () {
            (async () => {
                try {
                    const reviews = await fetchReviews();
                    if (reviews.length === 0) {
                        displayError('No reviews found on the page.', 'No reviews found on the page.');
                        return;
                    }
                    sendTaskRequest(currentUrl, reviews);
                } catch (e) {
                    console.error('Cannot access page:', e);
                }
            })();
        });

        function sendTaskRequest(url, reviewList) {

            const reviewMap = createReviewContentMap(reviewList);
            localStorage.setItem('reviewMap', JSON.stringify(reviewMap)); // Store the map

            const requestBody = {
                "client_id": getOrGenerateUUID(), "url": url, "reviews": reviewList
            };

            fetch(ec2_url + '/send_request', {
                method: 'POST', headers: {
                    'Content-Type': 'application/json'
                }, body: JSON.stringify(requestBody)
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data && data.status === 'ok' && data.message && data.message.task_id) {
                        const taskId = data.message.task_id;
                        console.log('Received Task ID:', taskId);

                        startTaskRequest(taskId, function () {
                            ldsRing.style.display = 'none';
                        });

                    } else {
                        throw new Error('Invalid response format or missing task_id');
                    }
                })
                .catch(error => {
                    displayError('Server is currently not available.', error);
                });
        }


        function startTaskRequest(taskId, callback) {
            const tableBody = document.querySelector('.styled-table tbody');
            const tableHead = document.querySelector('.styled-table thead');

            const secondRequestBody = {
                "client_id": getOrGenerateUUID(), "task_id": taskId
            };

            const pollInterval = 3000;
            let pollCount = 0;

            const pollScore = () => {
                console.log('Polling for task ID:', taskId);
                fetch(ec2_url + '/get_response', {
                    method: 'POST', headers: {
                        'Content-Type': 'application/json'
                    }, body: JSON.stringify(secondRequestBody)
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data && data.status === 'ok' && data.message && data.message.reviews !== undefined) {
                            console.log('Received response for task ID:', taskId);
                            if (data.message.reviews.length === 0) {
                                displayError('No reviews found on the page.', 'No reviews found on the page.')
                            } else {
                                // Clear previous content
                                tableBody.innerHTML = '';
                                tableHead.innerHTML = '';

                                let net_ids = ["as99", "bui5", "romanov2"]

                                // Populate table with new data
                                createTableHeader(net_ids);
                                const reviews = data.message.reviews;
                                populateTableWithReviews(reviews, net_ids);

                                // Hide the loading animation
                                ldsRing.style.display = 'none';

                                createButton();

                                if (typeof callback === "function") {
                                    callback();
                                }
                            }
                        } else {
                            if (pollCount < 20) { // Continue polling for a set amount of time
                                pollCount++;
                                setTimeout(pollScore, pollInterval);
                            } else {
                                // Handle the case when polling exceeds the limit
                                displayError('Server is currently not available.', 'Polling limit exceeded')
                            }
                        }
                    })
                    .catch(error => {
                        displayError('Server is currently not available.', error);
                    });
            };
            pollScore();
        }

        function populateTableWithReviews(reviews, net_ids) {
            const tableBody = document.querySelector('.styled-table tbody');
            const reviewMap = JSON.parse(localStorage.getItem('reviewMap'));

            const orderedReviews = [];

            // Iterate over the reviews object
            Object.entries(reviews).forEach(([reviewId, review]) => {
                const hash = simpleHash(review.content);
                const originalIndex = reviewMap[hash];
                if (originalIndex !== undefined) {
                    orderedReviews[originalIndex] = review;
                }
            });

            // Fill in any missing reviews to maintain the correct order
            for (let i = 0; i < orderedReviews.length; i++) {
                if (!orderedReviews[i]) {
                    orderedReviews[i] = {content: "Review not available", sentiment: {}};
                }
            }

            orderedReviews.forEach(review => {
                if (review) { // Check if the review is not null or undefined
                    const content = "\"" + review.content.substring(0, 100) + "...\"";
                    const sentiment = review.sentiment;

                    const tr = document.createElement('tr');
                    const contentCell = document.createElement('td');
                    contentCell.textContent = content;
                    tr.appendChild(contentCell);

                    for (const key in sentiment) {
                        if (net_ids.includes(key)) {
                            if (Object.prototype.hasOwnProperty.call(sentiment, key)) {
                                const score = sentiment[key];
                                const sentimentCell = document.createElement('td');
                                const icon = document.createElement('img');
                                icon.classList.add('sentiment-icon');

                                // Assign icons based on the sentiment score
                                if (score === 1) {
                                    icon.src = './Icons/lol.png';
                                    icon.alt = 'Happy';
                                } else if (score === 0) {
                                    icon.src = './Icons/neutral (1).png';
                                    icon.alt = 'Neutral';
                                } else if (score === -1) {
                                    icon.src = './Icons/angry.png';
                                    icon.alt = 'Angry';
                                } else {
                                    icon.src = './Icons/not-available-circle.png';
                                    icon.alt = 'N/A';
                                }

                                sentimentCell.appendChild(icon);
                                tr.appendChild(sentimentCell);
                            }
                        }
                    }
                    tableBody.appendChild(tr);
                } else {
                    console.error('Review not found in reviewMap');
                }
            });
        }


        document.addEventListener('click', function (event) {
            if (event.target.classList.contains('button-1')) {
                const nextPageButton = document.querySelector('.button-1');
                nextPageButton.disabled = true;

                chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
                    const activeTab = tabs[0];
                    let url = new URL(activeTab.url);

                    let pageNumber = 1;
                    const pageNumberParam = url.searchParams.get('pageNumber');
                    if (pageNumberParam !== null) {
                        pageNumber = parseInt(pageNumberParam, 10);
                    }

                    pageNumber++;
                    url.searchParams.set('pageNumber', pageNumber);

                    // Show loading animation
                    const ldsRing = document.querySelector('.lds-ring');
                    ldsRing.style.display = 'inline-block';

                    chrome.tabs.update(activeTab.id, {url: url.toString()});
                });
            }
        });
    }
});