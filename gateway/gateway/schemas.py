from marshmallow import Schema, fields


class CreateOrderDetailSchema(Schema):
    product_id = fields.Str(required=True)
    price = fields.Decimal(as_string=True, required=True)
    quantity = fields.Int(required=True)


class CreateOrderSchema(Schema):
    order_details = fields.Nested(
        CreateOrderDetailSchema, many=True, required=True
    )
    
class UpdateProductSchema(Schema):
    title = fields.String(required=False)
    passenger_capacity = fields.Integer(required=False)
    maximum_speed = fields.Integer(required=False)
    in_stock = fields.Integer(required=False)

class ProductSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    maximum_speed = fields.Int(required=True)
    in_stock = fields.Int(required=True)
    passenger_capacity = fields.Int(required=True)


class GetOrderSchema(Schema):

    class OrderDetail(Schema):
        id = fields.Int()
        quantity = fields.Int()
        product_id = fields.Str()
        image = fields.Str()
        price = fields.Decimal(as_string=True)
        product = fields.Nested(ProductSchema, many=False)

    id = fields.Int()
    order_details = fields.Nested(OrderDetail, many=True)
