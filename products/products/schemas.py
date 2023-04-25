from marshmallow import Schema, fields


class Product(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    passenger_capacity = fields.Int(required=True)
    maximum_speed = fields.Int(required=True)
    in_stock = fields.Int(required=True)


class UpdateProduct(Schema):
    title = fields.Str(required=False)
    passenger_capacity = fields.Int(required=False)
    maximum_speed = fields.Int(required=False)
    in_stock = fields.Int(required=False)
