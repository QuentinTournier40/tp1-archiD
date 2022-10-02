import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]

# root message

# ADMINS SERVICES
@app.route("/movie/<movieid>", methods=['PUT'])
def update_movie_rating(movieid):
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["id"]) == str(movieid):
                movie["rating"] = float(req["rate"])
                res = make_response(jsonify(movie), 200)
                return res

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


@app.route("/movie/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    res = make_response(jsonify({"message": "movie added"}), 201)
    return res


@app.route("/movie/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


# DEVELOPERS SERVICES
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


@app.route("/json", methods=['GET'])
def get_json():
    res = json.loads('{"movies": ' + json.dumps(movies) + '}')
    return make_response(jsonify(res), 200)


@app.route("/movie/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)

@app.route("/get-movie-by-movieid-imdb/<movieid>", methods=['GET'])
def get_movie_byid_imbd(movieid):
    data = requests.get('https://imdb-api.com/en/API/Title/k_84p059su/' + movieid).json()
    if not data['errorMessage'] is None:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    obj = {}
    obj["id"] = data["id"]
    obj["title"] = data["title"]
    obj["directors"] = data["directorList"]
    obj["type"] = data["type"]
    obj["year"] = data["year"]
    obj["runtimeMins"] = data["runtimeMins"]
    return make_response(jsonify(obj), 200)

@app.route("/moviebytitle/<title>", methods=['GET'])
def get_movie_bytitle(title):
    json = ""
    for movie in movies:
        if str(movie["title"]) == str(title):
            json = movie

    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res

@app.route("/get-movies-by-title-imdb/<title>", methods=['GET'])
def get_movies_bytitle_imdb(title):
    data = requests.get("https://imdb-api.com/en/API/SearchMovie/k_7ps4x3m7/" + title)
    if data.status_code == 200 and data.json()["results"]:
        movieJson = {}
        movieJson["movies"] = data.json()["results"]
        return make_response(jsonify(movieJson), 200)
    else:
        return make_response(jsonify({"error": "movie not found"}), 400)

@app.route("/moviesbydirector/<director>", methods=['GET'])
def get_movies_bydirector(director):
    moviesInfos = {}
    for movie in movies:
        if str(movie["director"]) == str(director):
            moviesInfos["movies"].append(movie)

    if not moviesInfos:
        res = make_response(jsonify({"error": "movies of this director not found"}), 400)
    else:
        res = make_response(jsonify(moviesInfos), 200)
    return res

@app.route("/get-ratings-by-movieid-imdb/<movieid>", methods=['GET'])
def get_ratings_by_movieid_imbd(movieid):
    ratingsInfos = requests.get('https://imdb-api.com/en/API/UserRatings/k_84p059su/' + movieid).json()
    if ratingsInfos['errorMessage']:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    ratings = {}
    ratings["ratings"] = ratingsInfos['ratings']
    return make_response(jsonify(ratings), 200)

@app.route("/api-discover", methods=['GET'])
def get_api_discover():
    allRoutes = {}
    allRoutes["routes"] = []
    for r in app.url_map._rules:
        route = {}
        route["path"] = r.rule
        route["functionName"] = r.endpoint
        route["methods"] = list(r.methods)
        allRoutes["routes"].append(route)
    return make_response(jsonify(allRoutes), 200)

if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
