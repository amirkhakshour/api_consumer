from api_consumer.endpoints.people import People
TEST_FILM_1_UUID = "2baf70d1-42bb-4437-b551-e5fed5a87abe"
TEST_FILM_2_UUID = "0440483e-ca0e-4120-8c50-4c8cd9b965d6"

TEST_PEOPLE_RESPONSE = [
    {
        "id": "ba924631-068e-4436-b6de-f3283fa848f0",
        "name": "Pazu",
        "gender": "Male",
        "films": [
            f"https://ghibliapi.herokuapp.com/films/{TEST_FILM_1_UUID}",
        ],
        "age": "age",
        "eye_color": "eye color",
        "hair_color": "hair color",
        "species": "species 1",
        "url": "url",
    },
    {
        "id": "ebe40383-aad2-4208-90ab-698f00c581ab",
        "name": "Lusheeta Toel Ul Laputa",
        "films": [
            f"https://ghibliapi.herokuapp.com/films/{TEST_FILM_1_UUID}",
            f"https://ghibliapi.herokuapp.com/films/{TEST_FILM_2_UUID}"
        ],
        "age": "age",
        "eye_color": "eye color",
        "hair_color": "hair color",
        "species": "species 1",
        "url": "url",
    }
]

TEST_MOVIE_1_RESPONSE = {
    "id": TEST_FILM_1_UUID,
    "title": "Movie 1",
    "description": "description 1",
    "director": "director 1",
    "producer": "producer 1",
    "people": [
        "https://ghibliapi.herokuapp.com/people/2baf70d1-42bb-4437-b551-e5fed5a87ab2"
    ],
    "release_date": 1957,
    "rt_score": 3,
    "species": ["species 1"],
    "locations": [],
    "vehicles": [],
    "url": "",
    "length": "",
}
TEST_MOVIE_2_RESPONSE = {
    "id": TEST_FILM_2_UUID,
    "title": "Movie 2",
    "description": "description 2",
    "director": "director 2",
    "producer": "producer 2",
    "people": [
        "https://ghibliapi.herokuapp.com/people/ba924631-068e-4436-b6de-f3283fa848f0",
        "https://ghibliapi.herokuapp.com/people/ebe40383-aad2-4208-90ab-698f00c581ab"
    ],
    "release_date": 1957,
    "rt_score": 3,
    "species": ["species 1"],
    "locations": [],
    "vehicles": [],
    "url": "",
    "length": "",
}


class TestPeopleAPIEndpoint:
    def test_nested_by_films(self, request_mock):
        request_mock.stub_request(
            "get",
            "people",
            TEST_PEOPLE_RESPONSE,
        )
        request_mock.stub_request(
            "get",
            f"films/{TEST_FILM_1_UUID}",
            TEST_MOVIE_1_RESPONSE,
        )
        request_mock.stub_request(
            "get",
            f"films/{TEST_FILM_2_UUID}",
            TEST_MOVIE_2_RESPONSE,
        )
        result = People.nested_by_films()
        assert sorted(list(result.keys())) == sorted([TEST_FILM_1_UUID, TEST_FILM_2_UUID])
        assert len(result[TEST_FILM_1_UUID]['people']) == 2
        assert len(result[TEST_FILM_2_UUID]['people']) == 1

        # probably test people in each movie
