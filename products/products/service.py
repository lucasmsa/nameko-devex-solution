import logging

from nameko.events import event_handler
from nameko.rpc import rpc
from products import dependencies, schemas


logger = logging.getLogger(__name__)


class ProductsService:

    name = 'products'

    storage = dependencies.Storage()

    @rpc
    def get(self, product_id):
        product = self.storage.get(product_id)
        return schemas.Product().dump(product).data

    @rpc
    def list(self, filter_title_term='', page=1, per_page=10):
        product_generator, total_products = self.storage.list(filter_title_term, page, per_page)
        products = list(product_generator)
        return {
            'products': schemas.Product(many=True).dump(products).data,
            'total_products': total_products
        }

    @rpc
    def create(self, product):
        product = schemas.Product(strict=True).load(product).data
        self.storage.create(product)
        
    @rpc
    def delete(self, product_id):
        self.storage.delete(product_id)
        
    @rpc
    def update(self, product_id, updated_fields):
        schema = schemas.UpdateProduct(strict=True)
        valid_fields = schema.load(updated_fields).data
        self.storage.update(product_id, valid_fields)

    @event_handler('orders', 'order_created')
    def handle_order_created(self, payload):
        for product in payload['order']['order_details']:
            self.storage.decrement_stock(
                product['product_id'], product['quantity'])
