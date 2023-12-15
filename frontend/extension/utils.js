const ec2_url = 'http://ec2-34-239-197-4.compute-1.amazonaws.com:8080'

function generateUUID() {
    /**
     * Generates a random UUID
     * @see https://stackoverflow.com/a/2117523/6777359
     */
    return 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function getOrGenerateUUID() {
    /**
     * Gets the UUID from localStorage, or generates a new one if it doesn't exist
     * @type {string} UUID
     */
    let uuid = localStorage.getItem('410UUID');
    if (!uuid) {
        uuid = generateUUID();
        localStorage.setItem('410UUID', uuid);
    }
    return uuid;
}

function createTableHeader(net_ids) {
    const headers = ["Review"].concat(net_ids);
    const tableHead = document.querySelector('.styled-table thead');

    if (tableHead.children.length === 0) {
        const head = document.createElement('tr');
        for (let i = 0; i < headers.length; i++) {
            const headerCell = document.createElement('th');
            headerCell.textContent = headers[i];
            head.appendChild(headerCell);
        }
        tableHead.appendChild(head);
    }
}

function isReviewPage(url) {
    if (url === undefined) return false;
    return url.includes('amazon.com') && url.includes('/product-reviews/');
}

function isProductPage(url) {
    if (url === undefined) return false;
    return url.includes('amazon.com') && url.includes('/dp/');
}

function displayErrorMessage(message) {

    if (message === undefined) {
        message = 'An unknown error occurred.';
    }

    const errorMsg = document.getElementById('error-msg');
    errorMsg.innerHTML = '<p class="error-text">' + message + '</p>';
}

function createReviewContentMap(reviewList) {
    const reviewMap = {};
    reviewList.forEach((review, index) => {
        const hash = simpleHash(review);
        reviewMap[hash] = index;
    });
    return reviewMap;
}

function simpleHash(input) {
    /**
     * Generates a simple hash of a string
     * @see https://stackoverflow.com/a/7616484/6777359
     */

    if (input === undefined || input.length === 0) return "0";

    let hash = 0;
    for (let i = 0; i < input.length; i++) {
        const char = input.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash.toString();
}
