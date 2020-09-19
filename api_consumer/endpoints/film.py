from api_consumer.endpoints import abc
from marshmallow import Schema, fields


class FilmEndpointSchema(Schema):
    id = fields.UUID()
    title = fields.String()
    description = fields.String()


class Film(abc.APIEndpointSchemaConverter, abc.APIEndpoint):
    name = "film"
    obj_name = "films"
    schema = FilmEndpointSchema
