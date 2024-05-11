import os
import redis
import pika
import json

import woody

redis_host = os.environ.get('REDIS_HOST')
cache = None

rabbitmq_host = os.environ.get('RABBITMQ_HOST')

def is_redis_available():
    try:
        cache.ping()
    except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError, redis.exceptions.TimeoutError):
        return False
    return True


def redis_connect():
    global cache
    for x in range(3):
        cache = redis.Redis(host=redis_host, port=6379)
        if is_redis_available():
            return True
    return False


# #### 4. internal Services
def process_order(order_id, order):
    # ...
    # ... do many check and stuff
    key_validation = f'validation_{order}'
    status = None
    if redis_connect():
        status = cache.get(key_validation)
    if not status:
        status = woody.make_heavy_validation(order)
        cache.setex(key_validation, 3600, status)

    woody.save_order(order_id, status, order)


def callback(ch, method, properties, body):
    data = json.loads(body)
    order_id = data['order_id']
    product = data['product']

    print(f'Processing... id: {order_id}, product: {product}')

    process_order(order_id, product)


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='order_queue', durable=True)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='order_queue', auto_ack=True, on_message_callback=callback)

channel.start_consuming()
