from functools import lru_cache
from marshmallow import Schema, fields, EXCLUDE
from api_consumer.endpoints import abc
from api_consumer.endpoints.film import Film, FilmEndpointSchema


class PeopleEndpointSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    gender = fields.String()
    films = fields.Method(data_key="films", deserialize="load_films")

    @lru_cache
    def extract_film_uuid(self, film_uuids):
        return film_uuids.rsplit("/", 1)[-1]

    def load_films(self, film_uuids):
        films = []
        for _uuid in film_uuids:
            film_uuid = self.extract_film_uuid(_uuid)
            film = Film.retrieve(_id=film_uuid)
            films.append(FilmEndpointSchema().load(film, unknown=EXCLUDE))
        return films


class People(abc.APIEndpointSchemaConverter, abc.APIEndpoint):
    name = "people"
    obj_name = "people"
    schema = PeopleEndpointSchema
