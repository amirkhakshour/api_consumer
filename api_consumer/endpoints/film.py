from api_consumer.endpoints import abc
from marshmallow import Schema, fields


class FilmEndpointSchema(Schema):
    id = fields.UUID()
    title = fields.String()
    description = fields.String()
    director = fields.String()
    producer = fields.String()
    release_date = fields.Integer()
    rt_score = fields.Integer()
    people = fields.List(fields.String)
    species = fields.List(fields.String)
    locations = fields.List(fields.String)
    vehicles = fields.List(fields.String)
    url = fields.String()
    length = fields.String(allow_none=True)


class Film(abc.APIEndpointSchemaConverter, abc.APIEndpoint):
    name = "film"
    obj_name = "films"
    schema = FilmEndpointSchema
