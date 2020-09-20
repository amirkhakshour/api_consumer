from flask import Flask, jsonify
from api_consumer.endpoints.people import People

app = Flask(__name__)


@app.route('/')
def index():
    return "ghibliapi API integration!"


@app.route('/movies', methods=['GET'])
def movies():
    output = People.nested_by_films()
    return jsonify(list(output.values()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
