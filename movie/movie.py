import requests
from flask import Flask, render_template, request, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3200
HOST = 'localhost'

with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]

# --------------------------- ADMINS SERVICES ---------------------------

# Fonction crée par Tournier Quentin et Marche Jules
# But: Modifier le rate d'un movie
# En entrée: IdMovie (path)
#            rate (query)
# En sortie: Json de l'objet modifié
@app.route("/movie/<movieid>", methods=['PUT'])
def update_movie_rating(movieid):
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["id"]) == str(movieid):
                movie["rating"] = float(req["rate"])
                return make_response(jsonify(movie), 200)

    return make_response(jsonify({"error": "movie ID not found"}), 400)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Créer un movie
# En entrée: IdMovie (path)
#            l'objet (body)
# En sortie: Un message stipulant la création de l'objet
@app.route("/movie/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    return make_response(jsonify({"message": "movie added"}), 201)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Supprimer un movie
# En entrée: IdMovie (path)
# En sortie: L'objet supprimé
@app.route("/movie/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    return make_response(jsonify({"error": "movie ID not found"}), 400)

# --------------------------- DEVELOPERS SERVICES ---------------------------

@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher une template HTML
# En entrée:
# En sortie: Un HTML
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher tous les objets de la BDD
# En entrée:
# En sortie: Un tableau de tous les objets de la BDD
@app.route("/json", methods=['GET'])
def get_json():
    return make_response(jsonify({"movies": movies}), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher un movie
# En entrée: IdMovie(path)
# En sortie: L'objet Movie en question
@app.route("/movie/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify(movie), 200)
    return make_response(jsonify({"error": "Movie ID not found"}), 400)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher un movie de la BDD IMDB
# En entrée: IdMovie(path)
# En sortie: L'objet en question
@app.route("/get-movie-by-movieid-imdb/<movieid>", methods=['GET'])
def get_movie_byid_imbd(movieid):
    data = requests.get('https://imdb-api.com/en/API/Title/k_84p059su/' + movieid).json()
    if data['errorMessage'] is not None:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    obj = {
        "id": data["id"],
        "title": data["title"],
        "directors": data["directorList"],
        "type": data["type"],
        "year": data["year"],
        "runtimeMins": data["runtimeMins"]
    }
    return make_response(jsonify(obj), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher un movie de la BDD par son titre
# En entrée: titre(path)
# En sortie: L'objet en question
@app.route("/moviebytitle/<title>", methods=['GET'])
def get_movie_bytitle(title):
    json = ""
    for movie in movies:
        if str(movie["title"]) == str(title):
            json = movie

    if not json:
        return make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        return make_response(jsonify(json), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher un movie de la BDD IMDB par son titre
# En entrée: titre(path)
# En sortie: L'objet en question
@app.route("/get-movies-by-title-imdb/<title>", methods=['GET'])
def get_movies_bytitle_imdb(title):
    data = requests.get("https://imdb-api.com/en/API/SearchMovie/k_7ps4x3m7/" + title)
    dataJson = data.json()
    if data.status_code == 200 and dataJson["results"]:
        return make_response(jsonify({"movies": dataJson["results"]}), 200)
    else:
        return make_response(jsonify({"error": "movie not found"}), 400)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher tous les movies d'un directeur
# En entrée: directeur(path)
# En sortie: Un tableau de tous les movies
@app.route("/moviesbydirector/<director>", methods=['GET'])
def get_movies_bydirector(director):
    moviesInfos = {"movies": []}
    for movie in movies:
        if str(movie["director"]) == str(director):
            moviesInfos["movies"].append(movie)

    if not moviesInfos:
        return make_response(jsonify({"error": "movies of this director not found"}), 400)
    else:
        return make_response(jsonify(moviesInfos), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher les notes d'un movie de la BDD IMDB
# En entrée: IdMovie(path)
# En sortie: Un tableau de tous les notes
@app.route("/get-ratings-by-movieid-imdb/<movieid>", methods=['GET'])
def get_ratings_by_movieid_imbd(movieid):
    ratingsInfosJson = requests.get('https://imdb-api.com/en/API/UserRatings/k_84p059su/' + movieid).json()
    if ratingsInfosJson['errorMessage']:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    return make_response(jsonify({"ratings" : ratingsInfosJson['ratings']}), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher l'ensemble des endpoints de l'api
# En entrée:
# En sortie: Un tableau de tous les endpoints
@app.route("/api-discover", methods=['GET'])
def get_api_discover():
    allRoutes = {"routes" : []}
    for r in app.url_map._rules:
        route = {
            "path": r.rule,
            "functionName": r.endpoint,
            "methods": list(r.methods)
        }
        allRoutes["routes"].append(route)
    return make_response(jsonify(allRoutes), 200)

if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
