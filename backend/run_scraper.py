import asyncio
import aio_pika
import json
import requests

from webutils import db_handler, rmq_handler
from webutils.utils import calculate_md5_hash

SCRAPER_URL = "http://localhost:5000/?url="

async def scrape(task_id, product_url):
    reviews = {}

    try:
      response = requests.get(SCRAPER_URL + product_url, headers={"Content-Type": "application/json",})
    except:
      return reviews

    reviews = {}

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            reviews = {calculate_md5_hash(review['content']): review['content'] for review in data['reviews']}
    else:
        pass
        # raise Exception("Error:", response.status_code, response.text)

    return reviews

async def repeated_scrape(task_id, product_url):
    max_attempts = 30
    while max_attempts > 0:
        reviews = await scrape(task_id, product_url)

        if len(reviews) > 0:
            break

        max_attempts -= 1
        await asyncio.sleep(0.5)

    return reviews

async def callback(message):
    async with message.process():
        body = json.loads(message.body.decode())
        print(f"Received message: {body}")

        db_handler.insert_task(body)

        body['reviews'] = await repeated_scrape(body['task_id'], body['url'])

        db_handler.insert_reviews(body['task_id'], body['reviews'])
        rmq_handler.publish_message(body, queue_name="scraper_messages")

        print(f"Scraper: task {body['task_id']} is finished")

async def main():
    connection = await aio_pika.connect_robust()
    channel = await connection.channel()
    queue = await channel.declare_queue("ws_messages")

    await queue.consume(callback)

    print("Press Ctrl+C to exit")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await connection.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
