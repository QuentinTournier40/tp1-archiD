from flask import Flask, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtime", methods=['GET'])
def get_schedule():
   return make_response(jsonify(schedule), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Affichez les films diffusés à la date donnée
# En entrée: date(path)
# En sortie: les films diffusés à la date passé en paramètre, ansi que le date
@app.route("/show-movies/<date>", methods=['GET'])
def get_movies_bydate(date):
   for dailySchedule in schedule:
      if str(dailySchedule["date"]) == str(date):
         return make_response(jsonify(dailySchedule), 200)
   return make_response(jsonify({"error":"schedule with this date not found"}), 400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
