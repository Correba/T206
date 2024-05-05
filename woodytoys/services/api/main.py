import uuid
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

import woody

import os
import redis

app = Flask('my_api')
cors = CORS(app)

redis_host = os.environ.get('REDIS_HOST')
cache = None

def is_redis_available():
    try:
        cache.ping()
    except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
        return False
    return True


def redis_connect():
    global cache
    for x in range(3):
        cache = redis.Redis(host=redis_host, port=6379)
        if is_redis_available():
            return True
    return False
    

@app.get('/api/ping')
def ping():
    return 'ping'


# ### 1. Misc service ### (note: la traduction de miscellaneous est 'divers'
@app.route('/api/misc/time', methods=['GET'])
def get_time():
    return f'misc: {datetime.now()}'


@app.route('/api/misc/heavy', methods=['GET'])
def get_heavy():
    # TODO TP9: cache ?
    name = request.args.get('name')
    key = f'heavy_{name}'
    if redis_connect():
        heavy = cache.get(key)
    if heavy is None:
        heavy = woody.make_some_heavy_computation(name)
        cache.setex(key, 3600, heavy)
    # on rajoute la date pour pas que le resultat ne soit mis en cache par le browser
    return f'{datetime.now()}: {heavy}'


# ### 2. Product Service ###
@app.route('/api/products', methods=['GET'])
def add_product():
    # product = request.json.get('product', '')
    product = request.args.get('product')
    if product:
        woody.add_product(str(product))
    return str(product) or "none"


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return "not yet implemented"


@app.route('/api/products/last', methods=['GET'])
def get_last_product():
    # TODO TP9: put in cache ? cache duration ?
    key = 'last_product'
    if redis_connect():
        cached_last_product = cache.get(key)

    if not cached_last_product:
        last_product = woody.get_last_product()  # note: it's a very slow db query
        cache.setex(key, 3600, last_product)
        return f'db: {datetime.now()} - {last_product}'
    return f'cache: {datetime.now()} - {cached_last_product}'


# ### 3. Order Service
@app.route('/api/orders/do', methods=['GET'])
def create_order():
    # very slow process because some payment validation is slow (maybe make it asynchronous ?)
    # order = request.get_json()
    product = request.args.get('product')
    order_id = str(uuid.uuid4())

    # TODO TP10: this next line is long, intensive and can be done asynchronously ... maybe use a message broker ?
    process_order(order_id, product)

    return f"Your process {order_id} has been created"


@app.route('/api/orders/', methods=['GET'])
def get_order():
    order_id = request.args.get('order_id')
    status = woody.get_order(order_id)

    return f'order "{order_id}": {status}'


# #### 4. internal Services
def process_order(order_id, order):
    # ...
    # ... do many check and stuff
    key_validation = f'validation_{order}'
    if redis_connect():
        status = cache.get(key_validation)
    if not status:
        status = woody.make_heavy_validation(order)
        cache.setex(key_validation, 3600, status)

    woody.save_order(order_id, status, order)


if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)
