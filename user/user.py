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
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

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


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
