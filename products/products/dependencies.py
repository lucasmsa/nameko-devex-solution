import re
from nameko import config
from functools import lru_cache
from nameko.extensions import DependencyProvider
import redis

from products.exceptions import NotFound, Conflict


REDIS_URI_KEY = 'REDIS_URI'


class StorageWrapper:
    """
    Product storage

    A very simple example of a custom Nameko dependency. Simplified
    implementation of products database based on Redis key value store.
    Handling the product ID increments or keeping sorted sets of product
    names for ordering the products is out of the scope of this example.

    """

    NotFound = NotFound

    def _product_not_found(self, product_id):
        raise self.NotFound('Product ID {} does not exist'.format(product_id))

    def __init__(self, client):
        self.client = client

    def _format_key(self, product_id):
        return 'products:{}'.format(product_id)

    def _from_hash(self, document):
        return {
            'id': document[b'id'].decode('utf-8'),
            'title': document[b'title'].decode('utf-8'),
            'passenger_capacity': int(document[b'passenger_capacity']),
            'maximum_speed': int(document[b'maximum_speed']),
            'in_stock': int(document[b'in_stock'])
        }

    @lru_cache(maxsize=128)
    def get(self, product_id):
        product = self.client.hgetall(self._format_key(product_id))
        if not product:
            self._product_not_found(product_id)
        else:
            return self._from_hash(product)

    def list(self, filter_title_term='', page=1, per_page=10):
        keys = self.client.keys(self._format_key('*'))

        filtered_keys = []
        if filter_title_term:
            pattern = re.compile(f".*{filter_title_term}.*", re.IGNORECASE)
            for key in keys:
                product = self._from_hash(self.client.hgetall(key))
                if pattern.match(product['title']):
                    filtered_keys.append(key)
        else:
            filtered_keys = keys

        total_products = len(filtered_keys)

        if page and per_page:
            start = (page - 1) * per_page
            end = start + per_page
            paginated_keys = filtered_keys[start:end]
        else: 
            paginated_keys = filtered_keys

        def product_generator():
            for key in paginated_keys:
                yield self._from_hash(self.client.hgetall(key))

        return product_generator(), total_products

    def create(self, product):
        if self.client.exists(self._format_key(product['id'])):
            raise Conflict('Product ID {} already exists'.format(product['id']))
        
        self.client.hmset(
            self._format_key(product['id']),
            product)
        
    def delete(self, product_id):
        key = self._format_key(product_id)
        if not self.client.exists(key):
            self._product_not_found(product_id)
        else:
            self.client.delete(key)
        
    def update(self, product_id, updated_fields):
        if not self.client.exists(self._format_key(product_id)):
            raise NotFound('Product ID {} does not exist'.format(product_id))
        else:
            self.client.hmset(self._format_key(product_id), updated_fields)
        

    def decrement_stock(self, product_id, amount):
        return self.client.hincrby(
            self._format_key(product_id), 'in_stock', -amount)


class Storage(DependencyProvider):

    def setup(self):
        self.client = redis.StrictRedis.from_url(config.get(REDIS_URI_KEY))

    def get_dependency(self, worker_ctx):
        return StorageWrapper(self.client)
