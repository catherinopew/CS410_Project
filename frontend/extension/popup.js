async function fetchReviews() {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true});

    let result;
    try {
        [{result}] = await chrome.scripting.executeScript({
            target: {tabId: tab.id}, func: () => document.documentElement.innerHTML,
        });
    } catch (e) {
        throw e;
    }

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = result;
    const reviewContentElements = tempDiv.querySelectorAll('.review-text-content');

    let reviewList = [];
    reviewContentElements.forEach((element) => {
        reviewList.push(element.textContent.trim());
    });

    return reviewList;
}