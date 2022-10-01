from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>", 200)

@app.route("/get-movies-infos-of-selected-movies-by-userid/<userid>", methods=['GET'])
def get_movies_infos_of_selected_movies_by_userid(userid):
    moviesInfos = json.loads('{"movies": []}')
    for user in users:
        if str(user["id"]) == str(userid):
            booking = requests.get("http://172.16.123.230:3201/bookings/" + userid)

    if not 'booking' in locals():
        return make_response(jsonify({"error": "user for this userid not found"}), 400)

    if booking.status_code != 200:
        return make_response(jsonify({"error": "this userid doesn't have bookings"}), 400)

    for date in booking.json()["dates"]:
        for movieid in date["movies"]:
            movie = requests.get("http://172.16.124.168:3200/movie/" + movieid)
            moviesInfos["movies"].append(movie.json())

    return make_response(jsonify(moviesInfos), 200)

@app.route("/get-writers-by-movieid-imdb/<movieid>", methods=['GET'])
def get_writers_by_movieid_imdb(movieid):
    data = requests.get('https://imdb-api.com/en/API/FullCast/k_7ps4x3m7/' + movieid).json()
    if data['errorMessage']:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    res = {}
    res["writers"] = data["writers"]["items"]
    return make_response(jsonify(res), 200)

@app.route("/get-directors-by-movieid-imdb/<movieid>", methods=['GET'])
def get_directors_by_movieid_imbd(movieid):
    data = requests.get('https://imdb-api.com/en/API/FullCast/k_7ps4x3m7/' + movieid).json()
    if data['errorMessage']:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    res = {}
    res["directors"] = data["directors"]["items"]
    return make_response(jsonify(res), 200)

@app.route("/get-actors-by-movieid-imdb/<movieid>", methods=['GET'])
def get_actors_by_movieid_imbd(movieid):
    data = requests.get('https://imdb-api.com/en/API/FullCast/k_7ps4x3m7/' + movieid).json()
    if data['errorMessage']:
        return make_response(jsonify({"error":"Movie not found"}), 400)
    res = {}
    res["actors"] = data["actors"]
    return make_response(jsonify(res), 200)

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)