import asyncio
import aio_pika
import json
import concurrent.futures

# Importing analyzer functions for sentiment analysis
from analyzer.bert_clf.analyzer import get_bert_clf_score
from analyzer.siebert_clf.analyzer import get_siebert_clf_score
from analyzer.lr_clf.analyzer import get_lr_clf_score

# Importing utility functions
from webutils.utils import calculate_md5_hash
from webutils import db_handler, rmq_handler

# Unique students' identifiers for sentiment analysis results
UIDs = ('as99', 'romanov2', 'bui5', 'jlo10', 'vdara2')

# List of sentiment analysis functions corresponding to UIDs
sa_funcs = (get_bert_clf_score, get_siebert_clf_score, get_lr_clf_score, None, None)

# Function to retrieve sentiment scores for a task
async def get_scores(task_id, reviews):
    global UIDs, sa_funcs

    if not reviews or not isinstance(reviews, dict):
        return {}

    # Separate review IDs and review content
    pairs = list(reviews.items())
    reviews_id, reviews_context = zip(*pairs)

    # Use ThreadPoolExecutor for parallel execution of sentiment analysis functions
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(func, reviews_context) for func in sa_funcs if func is not None]
        concurrent.futures.wait(futures)

    # Combine the results into a dictionary with UIDs and review IDs
    scores = dict(zip(UIDs, [None]*len(UIDs)))
    for i, future in enumerate(futures):
       scores[UIDs[i]] = future.result()

    scores["review_id"] = reviews_id

    return scores

# Callback function for handling received messages from RabbitMQ
async def callback(message):
    async with message.process():
        # Decode the message body and print it
        body = json.loads(message.body.decode())
        print(f"Received message: {body}")

        # Calculate MD5 hash for each review and insert them into the database
        body['reviews'] = {calculate_md5_hash(review): review for review in body['reviews']}
        db_handler.insert_reviews(body['task_id'], body['reviews'])

        # Get sentiment scores for the reviews
        body['scores'] = await get_scores(body['task_id'], body["reviews"])

        # Update the database with sentiment scores and mark the task as done
        db_handler.update_reviews(body['task_id'], body['reviews'], body['scores'])
        status = "done" if body['reviews'] else "no reviews"
        db_handler.update_task(body['task_id'], status)

        print(f"Analyzer: task {body['task_id']} is finished")

# Main function for setting up RabbitMQ connection and consuming messages
async def main():
    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    # Declare the queue for receiving messages
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
