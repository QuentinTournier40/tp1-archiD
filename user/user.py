from flask import Flask, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3203
HOST = 'localhost'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>", 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher toutes les informations des movies réservés par l'utilisateur
# En entrée: UserId(path)
# En sortie: Un tableau de toutes les informations
@app.route("/get-movies-infos-of-selected-movies-by-userid/<userid>", methods=['GET'])
def get_movies_infos_of_selected_movies_by_userid(userid):
    moviesInfos = {"movies": []}
    booking = ""
    for user in users:
        if str(user["id"]) == str(userid):
            booking = requests.get("http://localhost:3201/bookings/" + userid)

    if not str(booking):
        return make_response(jsonify({"error": "user for this userid not found"}), 400)

    if booking.status_code != 200:
        return make_response(jsonify({"error": "this userid doesn't have bookings"}), 400)

    bookingJson = booking.json()
    for date in bookingJson["dates"]:
        for movieid in date["movies"]:
            movie = requests.get("http://localhost:3200/movie/" + movieid)
            moviesInfos["movies"].append(movie.json())

    return make_response(jsonify(moviesInfos), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher toutes les auteurs d'un movie de la BDD IMDB
# En entrée: MovieId(path)
# En sortie: Un tableau de tous les auteurs
@app.route("/get-writers-by-movieid-imdb/<movieid>", methods=['GET'])
def get_writers_by_movieid_imdb(movieid):
    dataJson = requests.get('https://imdb-api.com/en/API/FullCast/k_7ps4x3m7/' + movieid).json()
    if dataJson['errorMessage']:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    res = {"writers": dataJson["writers"]["items"]}
    return make_response(jsonify(res), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher toutes les directeurs d'un movie de la BDD IMDB
# En entrée: MovieId(path)
# En sortie: Un tableau de tous les directeurs
@app.route("/get-directors-by-movieid-imdb/<movieid>", methods=['GET'])
def get_directors_by_movieid_imbd(movieid):
    dataJson = requests.get('https://imdb-api.com/en/API/FullCast/k_7ps4x3m7/' + movieid).json()
    if dataJson['errorMessage']:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    res = {"directors": dataJson["directors"]["items"]}
    return make_response(jsonify(res), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher toutes les acteurs d'un movie de la BDD IMDB
# En entrée: MovieId(path)
# En sortie: Un tableau de tous les acteurs
@app.route("/get-actors-by-movieid-imdb/<movieid>", methods=['GET'])
def get_actors_by_movieid_imbd(movieid):
    dataJson = requests.get('https://imdb-api.com/en/API/FullCast/k_7ps4x3m7/' + movieid).json()
    if dataJson['errorMessage']:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    res = {"actors": dataJson["actors"]}
    return make_response(jsonify(res), 200)

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)