from nameko.events import EventDispatcher
from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession
from functools import lru_cache
from orders.exceptions import NotFound
from orders.models import DeclarativeBase, Order, OrderDetail
from orders.schemas import OrderSchema


class OrderServiceMixin:
    db = DatabaseSession(DeclarativeBase)

    @lru_cache(maxsize=100)
    def _get_order(self, order_id):
        order = self.db.query(Order).get(order_id)
        if not order:
            raise NotFound(f"Order with id {order_id} not found")
        return order


class OrderDetailServiceMixin:
    db = DatabaseSession(DeclarativeBase)

    def _get_order_details(self, order):
        return {od.id: od for od in order.order_details}


class OrdersService(OrderServiceMixin, OrderDetailServiceMixin):
    name = 'orders'

    event_dispatcher = EventDispatcher()

    @rpc
    def get_order(self, order_id):
        order = self._get_order(order_id)
        return OrderSchema().dump(order).data

    @rpc
    def list_orders(self, page=1, per_page=10):
        orders_query = self.db.query(Order)

        total_orders = orders_query.count()
        orders_query = orders_query.offset((page - 1) * per_page).limit(per_page)

        orders = orders_query.all()
        orders_data = OrderSchema(many=True).dump(orders).data

        return {
            'orders': orders_data,
            'page': page,
            'per_page': per_page,
            'total_orders': total_orders,
        }

    @rpc
    def create_order(self, order_details):
        order = Order(
            order_details=[
                OrderDetail(
                    product_id=order_detail['product_id'],
                    price=order_detail['price'],
                    quantity=order_detail['quantity']
                )
                for order_detail in order_details
            ]
        )
        self.db.add(order)
        self.db.commit()

        order = OrderSchema().dump(order).data

        self.event_dispatcher('order_created', {
            'order': order,
        })

        return order

    @rpc
    def update_order(self, order):
        order_details = {
            order_details['id']: order_details
            for order_details in order['order_details']
        }

        order = self._get_order(order['id'])

        for order_detail in order.order_details:
            order_detail.price = order_details[order_detail.id]['price']
            order_detail.quantity = order_details[order_detail.id]['quantity']

        self.db.commit()
        return OrderSchema().dump(order).data

    @rpc
    def delete_order(self, order_id):
        order = self._get_order(order_id)
        for order_detail in order.order_details:
            self.db.delete(order_detail)
        self.db.delete(order)
        self.db.commit()