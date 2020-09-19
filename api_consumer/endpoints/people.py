from functools import lru_cache
from marshmallow import Schema, fields, EXCLUDE
from api_consumer.endpoints import abc
from api_consumer.endpoints.film import Film, FilmEndpointSchema


class PeopleEndpointSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    gender = fields.String()
    films = fields.Method(data_key="films", deserialize="load_films")
    age = fields.String()
    eye_color = fields.String()
    hair_color = fields.String()
    species = fields.String()  # TODO load from Species endpoint
    url = fields.String()

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

    @classmethod
    def nested_by_films(cls):
        """Returns list of movies with list of people in each movie.
        :return:
        """
        output = dict()
        for people in cls.list():
            for film in people["films"]:
                # override people with empty list
                film["people"] = []
                film_uuid = str(film["id"])
                _people = dict(people)
                _people.pop("films")
                output.setdefault(film_uuid, film)
                output[film_uuid]["people"].append(_people)
        return output
