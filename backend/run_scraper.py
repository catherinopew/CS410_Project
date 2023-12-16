import asyncio
import aio_pika
import json
import requests

# Importing utility functions and handlers
from webutils import db_handler, rmq_handler
from webutils.utils import calculate_md5_hash

# URL of the scraper service
SCRAPER_URL = "http://localhost:5000/?url="

# Function to scrape reviews from a given product URL
async def scrape(task_id, product_url):
    reviews = {}

    try:
        # Make a GET request to the scraper service
        response = requests.get(SCRAPER_URL + product_url, headers={"Content-Type": "application/json",})
    except:
        # In case of an exception, return an empty reviews dictionary
        return reviews

    reviews = {}

    if response.status_code == 200:
        # If the response status code is 200, parse the JSON data
        data = response.json()
        if isinstance(data, dict):
            # Extract reviews and calculate MD5 hash for each
            reviews = {calculate_md5_hash(review['content']): review['content'] for review in data['reviews']}
    else:
        pass
        # raise Exception("Error:", response.status_code, response.text)

    return reviews

# Function to repeatedly scrape reviews with a maximum number of attempts
async def repeated_scrape(task_id, product_url):
    max_attempts = 30
    while max_attempts > 0:
        # Perform the scraping and break the loop if reviews are obtained
        reviews = await scrape(task_id, product_url)
        if len(reviews) > 0:
            break

        # Decrement the attempts counter and wait for 0.5 seconds before retrying
        max_attempts -= 1
        await asyncio.sleep(0.5)

    return reviews

# Callback function for handling received messages from RabbitMQ
async def callback(message):
    async with message.process():
        # Decode the message body and print it
        body = json.loads(message.body.decode())
        print(f"Received message: {body}")

        # Insert the task into the database
        db_handler.insert_task(body)

        # Scrape reviews repeatedly and insert them into the database
        body['reviews'] = await repeated_scrape(body['task_id'], body['url'])
        db_handler.insert_reviews(body['task_id'], body['reviews'])

        # Publish the message with reviews to another queue
        rmq_handler.publish_message(body, queue_name="scraper_messages")

        print(f"Scraper: task {body['task_id']} is finished")

# Main function for setting up RabbitMQ connection and consuming messages
async def main():
    connection = await aio_pika.connect_robust()
    channel = await connection.channel()
    queue = await channel.declare_queue("ws_messages")

    # Start consuming messages and pass them to the callback function
    await queue.consume(callback)

    print("Press Ctrl+C to exit")

    try:
        # Keep the event loop running until interrupted
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Close the RabbitMQ connection on interruption
        await connection.close()

# Entry point for the script
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
