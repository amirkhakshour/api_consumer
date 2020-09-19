# from marshmallow import Schema, fields, EXCLUDE
# from api_consumer.endpoints import abc
#
#
# class FilmSchema(Schema):
#     id = fields.UUID()
#     title = fields.String()
#     description = fields.String()
#
#
# class PeopleSchema(Schema):
#     id = fields.UUID()
#     name = fields.String()
#     gender = fields.String()
#     films = fields.Method(
#         data_key="films", deserialize="load_films"
#     )
#
#     def extract_film_uuid(self, film_uuids):
#         return film_uuids.rsplit('/', 1)[-1]
#
#     def load_films(self, film_uuids):
#         films = []
#         for _uuid in film_uuids:
#             print("_uuid", _uuid)
#             film_uuid = self.extract_film_uuid(_uuid)
#             film = Film.retrieve(_id=film_uuid)
#             films.append(FilmSchema().load(film, unknown=EXCLUDE))
#         return films
#
#
# class People(abc.APIEndpointSchemaConverter, abc.APIEndpoint):
#     name = "people"
#     obj_name = "people"
#     schema = PeopleSchema
#
#
# class Film(abc.APIEndpointSchemaConverter, abc.APIEndpoint):
#     name = "film"
#     obj_name = "film"
#     schema = FilmSchema
#
