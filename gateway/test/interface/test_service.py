import json

from mock import call

from gateway.exceptions import OrderNotFound, ProductNotFound


class TestGetProduct(object):
    def test_can_get_product(self, gateway_service, web_session):
        gateway_service.products_rpc.get.return_value = {
            "in_stock": 10,
            "maximum_speed": 5,
            "id": "the_odyssey",
            "passenger_capacity": 101,
            "title": "The Odyssey"
        }
        response = web_session.get('/products/the_odyssey')
        assert response.status_code == 200
        assert gateway_service.products_rpc.get.call_args_list == [
            call("the_odyssey")
        ]
        assert response.json() == {
            "in_stock": 10,
            "maximum_speed": 5,
            "id": "the_odyssey",
            "passenger_capacity": 101,
            "title": "The Odyssey"
        }

    def test_product_not_found(self, gateway_service, web_session):
        gateway_service.products_rpc.get.side_effect = (
            ProductNotFound('missing'))

        # call the gateway service to get order #1
        response = web_session.get('/products/foo')
        assert response.status_code == 404
        payload = response.json()
        assert payload['error'] == 'PRODUCT_NOT_FOUND'
        assert payload['message'] == 'missing'


class TestCreateProduct(object):
    def test_can_create_product(self, gateway_service, web_session):
        response = web_session.post(
            '/products',
            json.dumps({
                "in_stock": 10,
                "maximum_speed": 5,
                "id": "the_odyssey",
                "passenger_capacity": 101,
                "title": "The Odyssey"
            })
        )
        assert response.status_code == 200
        assert response.json() == {'id': 'the_odyssey'}
        
        assert gateway_service.products_rpc.create.call_args_list == [call({
                "in_stock": 10,
                "maximum_speed": 5,
                "id": "the_odyssey",
                "passenger_capacity": 101,
                "title": "The Odyssey"
            })]
        
    def test_create_product_fails_with_invalid_json(
        self, gateway_service, web_session
    ):
        response = web_session.post(
            '/products', 'NOT-JSON'
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'BAD_REQUEST'

    def test_create_product_fails_with_invalid_data(
        self, gateway_service, web_session
    ):
        response = web_session.post(
            '/products',
            json.dumps({"id": 1})
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'VALIDATION_ERROR'

class TestDeleteProduct(object):
    def test_can_delete_product(self, gateway_service, web_session):
        response = web_session.delete('/products/the_odyssey')
        assert response.status_code == 204
        assert gateway_service.products_rpc.delete.call_args_list == [
            call("the_odyssey")
        ]

    def test_product_not_found_on_delete(self, gateway_service, web_session):
        gateway_service.products_rpc.delete.side_effect = (
            ProductNotFound('missing'))

        response = web_session.delete('/products/foo')
        assert response.status_code == 404
        payload = response.json()
        assert payload['error'] == 'PRODUCT_NOT_FOUND'
        assert payload['message'] == 'missing'

class TestGetOrder(object):

    def test_can_get_order(self, gateway_service, web_session):
        # setup mock orders-service response:
        gateway_service.orders_rpc.get_order.return_value = {
            "order_details": [
                {
                    "product_id": "zd",
                    "product": {
                        "in_stock": 99,
                        "maximum_speed": 10,
                        "title": "The Hyndai",
                        "id": "zd",
                        "passenger_capacity": 201
                    },
                    "quantity": 1,
                    "price": "100000.99",
                    "image": "http://www.example.com/airship/images/zd.jpg",
                    "id": 21
                }
            ],
            "id": 21
        }

        # setup mock products-service response:
        gateway_service.products_rpc.get.return_value = {
            "in_stock": 250,
            "maximum_speed": 150,
            "title": "Zelda",
            "id": "zd",
            "passenger_capacity": 30
        }

        # call the gateway service to get order #1
        response = web_session.get('/orders/1')
    
        assert response.status_code == 200

        expected_response = {
            "order_details":[
                {
                    "image":"http://example.com/airship/images/zd.jpg",
                    "quantity":1,
                    "product_id":"zd",
                    "product":{
                        "title":"Zelda",
                        "maximum_speed":150,
                        "in_stock":250,
                        "passenger_capacity":30,
                        "id":"zd"
                    },
                    "price":"100000.99",
                    "id":21
                }
            ],
            "id":21
        }
        
        assert expected_response == response.json()

        # check dependencies called as expected
        assert [call(1)] == gateway_service.orders_rpc.get_order.call_args_list
        assert [call('zd')] == gateway_service.products_rpc.get.call_args_list

    def test_order_not_found(self, gateway_service, web_session):
        gateway_service.orders_rpc.get_order.side_effect = (
            OrderNotFound('missing'))

        # call the gateway service to get order #1
        response = web_session.get('/orders/1')
        assert response.status_code == 404
        payload = response.json()
        assert payload['error'] == 'ORDER_NOT_FOUND'
        assert payload['message'] == 'missing'


class TestGetOrders(object):
    def test_can_list_orders(self, gateway_service, web_session):
        # setup mock orders-service response:
        gateway_service.orders_rpc.list_orders.return_value = {
            "orders": [
                {
                    "order_details": [
                        {
                            "product_id": "the_odyssey",
                            "price": "100000.99",
                            "id": 1,
                            "quantity": 1
                        }
                    ],
                    "id": 1
                },
                {
                    "order_details": [
                        {
                            "product_id": "the_odyssey",
                            "price": "100000.99",
                            "id": 2,
                            "quantity": 1
                        }
                    ],
                    "id": 2
                }
            ],
            "page": 1,
            "per_page": 10,
            "total_orders": 2
        }

        response = web_session.get('/orders')
        
        assert response.status_code == 200
        assert gateway_service.orders_rpc.list_orders.call_args_list == [call(page=1, per_page=10)]
        
        assert response.json() == {
            "orders":[
                {
                    "order_details":[
                        {
                            "product_id":"the_odyssey",
                            "price":"100000.99",
                            "id":1,
                            "quantity":1
                        }
                    ],
                    "id":1
                },
                {
                    "order_details":[
                        {
                            "product_id":"the_odyssey",
                            "price":"100000.99",
                            "id":2,
                            "quantity":1
                        }
                    ],
                    "id":2
                }
            ],
            "page":1,
            "per_page":10,
            "total_orders":2
        }

    def test_empty_list_orders(self, gateway_service, web_session):
        gateway_service.orders_rpc.list_orders.return_value = {
            "orders": [],
            "page": 1,
            "per_page": 10,
            "total_orders": 0
        }

        response = web_session.get('/orders')
        assert response.status_code == 200
        assert gateway_service.orders_rpc.list_orders.call_args_list == [call(page=1, per_page=10)]
        assert response.json() == {
            'orders': [],
            'page': 1,
            "per_page": 10,
            "total_orders": 0
        }


class TestCreateOrder(object):

    def test_can_create_order(self, gateway_service, web_session):
        # setup mock products-service response:
        gateway_service.products_rpc.get.return_value = {
                "id": "zd",
                "maximum_speed": 150,
                "title": "Zelda",
                "in_stock": -250,
                "passenger_capacity": 30
            }

        # setup mock create response
        gateway_service.orders_rpc.create_order.return_value = {
            'id': 11,
            'order_details': []
        }

        # call the gateway service to create the order
        response = web_session.post(
            '/orders',
            json.dumps({
                'order_details': [
                    {
                        'product_id': 'zd',
                        'price': '41.00',
                        'quantity': 3
                    }
                ]
            })
        )
        assert response.status_code == 200
        assert response.json() == {'id': 11}
        assert gateway_service.products_rpc.get.call_args_list == [call('zd')]
        assert gateway_service.orders_rpc.create_order.call_args_list == [
            call([
                {'product_id': 'zd', 'quantity': 3, 'price': '41.00'}
            ])
        ]

    def test_create_order_fails_with_invalid_json(
        self, gateway_service, web_session
    ):
        # call the gateway service to create the order
        response = web_session.post(
            '/orders', 'NOT-JSON'
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'BAD_REQUEST'

    def test_create_order_fails_with_invalid_data(
        self, gateway_service, web_session
    ):
        # call the gateway service to create the order
        response = web_session.post(
            '/orders',
            json.dumps({
                'order_details': [
                    {
                        'product_id': 'the_odyssey',
                        'price': '41.00',
                    }
                ]
            })
        )
        
        assert response.status_code == 400
        assert response.json()['error'] == 'VALIDATION_ERROR'

    def test_create_order_fails_with_unknown_product(
        self, gateway_service, web_session
    ):
        # setup mock products-service response:
        gateway_service.products_rpc.get.side_effect = ProductNotFound('Product Id unknown')

        # call the gateway service to create the order
        response = web_session.post(
            '/orders',
            json.dumps({
                'order_details': [
                    {
                        'product_id': 'unknown',
                        'price': '41',
                        'quantity': 1
                    }
                ]
            })
        )
        assert response.status_code == 404
        assert response.json()['error'] == 'PRODUCT_NOT_FOUND'
        assert response.json()['message'] == 'Product Id unknown'
