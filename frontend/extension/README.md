## Overview
The extensions folder encapsulates the core functionalities of a Chrome extension designed for sentiment analysis on Amazon product review pages. It comprises various scripts responsible for interacting with the extension's UI, communicating with servers to retrieve and process data, and dynamically presenting analyzed review sentiments in a tabular format for user comprehension. The code implements event listeners, HTTP requests, table population logic, and data handling to seamlessly bridge the gap between user interaction and server-side processes, enhancing the user experience by offering clear insights into review sentiments.

## Files

### Icons folder
  This folder contains all of the icon images that were used for the extension UI, including the icons used to represent sentiments as well as the extension icons.

### content.js
The script is triggered upon DOM content loading, encompassing various functions interacting with the extension. It retrieves the active tab's URL, generates HTML elements like a specific button, and sends POST requests to a designated server URL, managing responses by checking for valid task IDs and initiating subsequent processes. One such process involves continuous server polling for specific task-related data, dynamically updating an HTML table with retrieved reviews and their sentiment information. Additionally, it controls loading bar display. The immediate execution of certain functions upon the DOMContentLoaded event and event listeners monitoring clicks on designated elements, such as the 'button-1' class, optimize user interaction by enabling dynamic tab URL updates and data fetching.

### manifest.json
This manifest outlines the extension's basic information, permissions required, allowed host access, icon specifications, and content scripts used for interaction with Amazon product review pages. 

### popup.css
The CSS styles define the visual appearance of the extension's user interface. It employs a responsive layout strategy using Flexbox, ensuring content alignment and consistent presentation. Various elements like tables for review display, loading animations, buttons, sentiment icons, extension name, and error messages are styled for visual consistency and clarity. These styles ensure a clean and organized interface, facilitating a seamless user experience within the extension's functionality.

### popup.html
This HTML file structures the popup interface for the extension. It includes various elements: a header displaying the extension's name and icon, a loading animation for sentiment analysis, a message about analysis duration, an error message display section, and a styled table container for reviews. It links to external CSS and JavaScript files for styling and functionality.

### popup.js
This asynchronous function fetches Amazon product review content from the active tab within a Chrome extension. It leverages Chrome's APIs to access the current tab's HTML content using chrome.scripting.executeScript(). It targets the .review-text-content elements, retrieving and formatting their text content into a list of review texts. The function then returns this list for further processing.

### utils.js
This block of code sets up essential functions and constants for handling Amazon product review pages within a Chrome extension. It includes functionalities to generate and retrieve UUIDs, create table headers, verify page types (review or product), display error messages, and create a map of review content. Additionally, it features a simple hash function used in generating unique identifiers for review content and contains a constant for an AWS EC2 URL used for server communication.