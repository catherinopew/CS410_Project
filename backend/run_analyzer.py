import asyncio
import aio_pika
import json

import concurrent.futures

from analyzer.bert_clf.analyzer import get_bert_clf_score
from analyzer.siebert_clf.analyzer import get_siebert_clf_score
from analyzer.lr_clf.analyzer import get_lr_clf_score
from webutils.utils import calculate_md5_hash
from webutils import db_handler, rmq_handler


UIDs = ('as99', 'romanov2', 'bui5', 'jlo10', 'vdara2')
sa_funcs = (get_bert_clf_score, get_siebert_clf_score, get_lr_clf_score, None, None)

async def get_scores(task_id, reviews):
    global UIDs, sa_funcs

    if not reviews or not isinstance(reviews, dict):
        return {}

    pairs = list(reviews.items())
    reviews_id, reviews_context = zip(*pairs)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(func, reviews_context) for func in sa_funcs if func is not None]
        concurrent.futures.wait(futures)

    scores = dict(zip(UIDs, [None]*len(UIDs)))
    for i, future in enumerate(futures):
       scores[UIDs[i]] = future.result()

    scores["review_id"] = reviews_id

    return scores

async def callback(message):
    async with message.process():
        body = json.loads(message.body.decode())
        print(f"Received message: {body}")

        body['reviews'] = {calculate_md5_hash(review): review for review in body['reviews']}
        db_handler.insert_reviews(body['task_id'], body['reviews'])

        body['scores'] = await get_scores(body['task_id'], body["reviews"])

        db_handler.update_reviews(body['task_id'], body['reviews'], body['scores'])

        status = "done" if body['reviews'] else "no reviews"
        db_handler.update_task(body['task_id'], status)

        print(f"Analyzer: task {body['task_id']} is finished")

async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/",)
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
