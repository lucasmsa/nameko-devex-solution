import json
import math
from marshmallow import ValidationError
from nameko import config
from nameko.exceptions import BadRequest
from nameko.rpc import RpcProxy
from werkzeug import Request, Response

from gateway.entrypoints import http
from gateway.exceptions import OrderNotFound, ProductNotFound, ProductAlreadyExists
from gateway.schemas import CreateOrderSchema, GetOrderSchema, ProductSchema, UpdateProductSchema


class GatewayService(object):
    """
    Service acts as a gateway to other services over http.
    """

    name = 'gateway'

    orders_rpc = RpcProxy('orders')
    products_rpc = RpcProxy('products')
    
    @http("GET", "/orders", expected_exceptions=OrderNotFound)
    def get_orders(self, request):
        req = Request(request.environ)

        page = int(req.args.get('page', 1))
        per_page = int(req.args.get('per_page', 10))

        orders = self.orders_rpc.list_orders(page=page, per_page=per_page)
    
        response_data = {
            'orders': orders['orders'],
            'page': orders['page'],
            'per_page': orders['per_page'],
            'total_orders': orders['total_orders'],
        }

        return Response(
            json.dumps(response_data),
            mimetype='application/json'
        )
        
    @http("DELETE", "/orders/<int:order_id>", expected_exceptions=OrderNotFound)
    def delete_order(self, request, order_id):
        """Deletes an existing order by `order_id`.
        """
        self.orders_rpc.delete_order(order_id)
        return Response(status=204)
    
    @http("GET", "/orders/<int:order_id>", expected_exceptions=OrderNotFound)
    def get_order(self, request, order_id):
        """Gets the order details for the order given by `order_id`.

        Enhances the order details with full product details from the
        products-service.
        """
        order = self._get_order(order_id)
        return Response(
            GetOrderSchema().dumps(order).data,
            mimetype='application/json'
        )

    def _get_order(self, order_id):
        # Retrieve order data from the orders service.
        # Note - this may raise a remote exception that has been mapped to
        # raise``OrderNotFound``
        order = self.orders_rpc.get_order(order_id)

        # get the configured image root
        image_root = config['PRODUCT_IMAGE_ROOT']

        # Enhance order details with product and image details.
        for item in order['order_details']:
            product_id = item['product_id']
            product = self.products_rpc.get(product_id)
            
            item['product'] = product
            # Construct an image url.
            item['image'] = '{}/{}.jpg'.format(image_root, product_id)

        return order

    @http(
        "POST", "/orders",
        expected_exceptions=(ValidationError, ProductNotFound, BadRequest)
    )
    def create_order(self, request):
        """Create a new order - order data is posted as json

        Example request ::

            {
                "order_details": [
                    {
                        "product_id": "the_odyssey",
                        "price": "99.99",
                        "quantity": 1
                    },
                    {
                        "price": "5.99",
                        "product_id": "the_enigma",
                        "quantity": 2
                    },
                ]
            }


        The response contains the new order ID in a json document ::

            {"id": 1234}

        """

        schema = CreateOrderSchema(strict=True)

        try:
            # load input data through a schema (for validation)
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.
            order_data = schema.loads(request.get_data(as_text=True)).data
            id_ = self._create_order(order_data)
        except ValueError as exc:
            raise BadRequest("Invalid json: {}".format(exc))
        except ProductNotFound as exc:
            raise ProductNotFound("{}".format(exc))

        return Response(json.dumps({'id': id_}), mimetype='application/json')

    def _create_order(self, order_data):
        # Check if order product IDs are valid
        for item in order_data['order_details']:
            product_id = item['product_id']
            self.products_rpc.get(product_id)

        # Call orders-service to create the order.
        # Dump the data through the schema to ensure the values are serialized
        # correctly.
        serialized_data = CreateOrderSchema().dump(order_data).data
        result = self.orders_rpc.create_order(
            serialized_data['order_details']
        )
        return result['id']
    
    
    @http("GET", "/products", expected_exceptions=ProductNotFound)
    def get_products(self, request):
        """Gets a list of products with optional filtering and pagination.
        
        These functionalities are exposed as query parameters, e.g.:
        
        Example request ::
            
            ?page=2&per_page=5&filter=odyssey
            
        The response contains a list of products, its page and the number of items per page in a json document ::

            {
                products: [...] # list of products
                page: 2,
                per_page: 5
            }
            
        """
        req = Request(request.environ)
        
        filter_title_term = req.args.get('filter', '')
        page = int(req.args.get('page', 1))
        per_page = int(req.args.get('per_page', 10))
        
        products = self.products_rpc.list(filter_title_term=filter_title_term, page=page, per_page=per_page)
        
        response_data = {
            'products': ProductSchema(many=True).dump(products['products']).data,
            'page': page,
            'per_page': per_page,
            'total_products': products['total_products']
        }
        
        return Response(
            json.dumps(response_data),
            mimetype='application/json'
        )
    
    @http(
        "GET", "/products/<string:product_id>",
        expected_exceptions=ProductNotFound
    )
    def get_product(self, request, product_id):
        """Gets product by `product_id`
        """
        product = self.products_rpc.get(product_id)
        return Response(
            ProductSchema().dumps(product).data,
            mimetype='application/json'
        )

    @http(
        "POST", "/products",
        expected_exceptions=(ValidationError, BadRequest)
    )
    def create_product(self, request):
        """Create a new product - product data is posted as json

        Example request ::

            {
                "id": "the_odyssey",
                "title": "The Odyssey",
                "passenger_capacity": 101,
                "maximum_speed": 5,
                "in_stock": 10
            }


        The response contains the new product ID in a json document ::

            {"id": "the_odyssey"}

        """

        schema = ProductSchema(strict=True)

        try:
            # load input data through a schema (for validation)
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.
            product_data = schema.loads(request.get_data(as_text=True)).data
            self.products_rpc.create(product_data)
        except ValueError as exc:
            raise BadRequest("Invalid json: {}".format(exc)) 
        except ProductAlreadyExists as exc:
            raise ProductAlreadyExists('{}'.format(exc))           

        # Create the product
        return Response(
            json.dumps({'id': product_data['id']}), mimetype='application/json'
        )
        
    # Add this method to GatewayService class
    @http(
        "PATCH", "/products/<string:product_id>",
        expected_exceptions=(ValidationError, BadRequest, ProductNotFound)
    )
    def update_product(self, request, product_id):
        """Update an existing product - updated product data is sent as json

        Example request ::

            {
                "title": "The Updated Odyssey",
                "passenger_capacity": 120,
                "maximum_speed": 6,
                "in_stock": 15
            }
            
            
        """

        schema = UpdateProductSchema(strict=True)

        try:
            # load input data through a schema (for validation)
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.
            updated_product_data = schema.loads(request.get_data(as_text=True)).data
        except ValueError as exc:
            raise BadRequest("Invalid json: {}".format(exc))

        # Update the product
        self.products_rpc.update(product_id, updated_product_data)

        return Response(status=204)  # 204 No Content indicates a successful update
        
    @http("DELETE", "/products/<string:product_id>", expected_exceptions=ProductNotFound)
    def delete_product(self, request, product_id):
        """Deletes an existing product by `product_id`
        """
        self.products_rpc.delete(product_id)
        return Response(status=204)
