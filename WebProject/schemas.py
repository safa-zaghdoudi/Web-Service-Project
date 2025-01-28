from marshmallow import Schema, fields

class ResidencySchema(Schema):
    id = fields.Str(dump_only=True)  # MongoDB ObjectID
    Residency_Type = fields.Str(required=True)
    Residency = fields.Str(required=True)
    city = fields.Str(required=True)
    Telephone = fields.Int()
    Adress = fields.Str()
    Available_transportation = fields.Str()
