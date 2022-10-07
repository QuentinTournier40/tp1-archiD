from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3201
HOST = 'localhost'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
   return make_response(jsonify(bookings), 200)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Afficher toutes les réservations d'un Utilisateur
# En entrée: UserId(path)
# En sortie: Un tableau de toutes les réservations
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         return make_response(jsonify(booking), 200)
   return make_response(jsonify({"error":"booking with this id not found"}),400)

# Fonction crée par Tournier Quentin et Marche Jules
# But: Ajouter une réservation à un utilisateur
# En entrée: UserId(path), movieid et date(body)
# En sortie: Un message stipulant l'ajout de la réservation ou d'erreur
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
   req = request.get_json()

   # Recupération des films diffusés à la date donnée
   sheduleJson = requests.get("http://localhost:3202/show-movies/" + str(req["date"])).json()
   sheduleExist = False

   # Check si l'utilisateur existe
   bookingOfUser = {}
   for booking in bookings:
      if booking["userid"] == str(userid):
         bookingOfUser = booking

   if not bool(bookingOfUser):
      return make_response(jsonify({"message": "UserId not found"}), 400)

   # Check si le film est diffusé à la date donnée
   for moviesShownId in sheduleJson["movies"]:
      if req["movieid"] == moviesShownId:
         sheduleExist = True

   if not sheduleExist:
      return make_response(jsonify({"message": "Movie not shown at this date"}), 400)

   # Check si l'utilisateur a deja reservé un film à la date demandée
   dateInfosOfBooking = {}
   for bookingDateInfo in bookingOfUser["dates"]:
      if bookingDateInfo["date"] == str(req["date"]):
         dateInfosOfBooking = bookingDateInfo

   # Si il a deja un film reservé à la date demandé il faut verifier que ce n'est pas celui qu'il demande maintenant
   if bool(dateInfosOfBooking):
      for movieid in dateInfosOfBooking["movies"]:
         if movieid == req["movieid"]:
            return make_response(jsonify({"error": "This booking already exists for this movie at this date"}), 409)

   # Mise à jour de la BDD
   indexBookingOfUser = bookings.index(bookingOfUser)
   if bool(dateInfosOfBooking):
      # Si l'user possède deja une reservation pour la date demandée
      indexDate = bookingOfUser["dates"].index(dateInfosOfBooking)
      bookingOfUser["dates"][indexDate]["movies"].append(req["movieid"])
   else:
      # Si l'user ne possède pas une reservation pour la date demandée
      bookingOfUser["dates"].append(req)

   bookings[indexBookingOfUser] = bookingOfUser
   return make_response(jsonify({"message": "booking added"}), 200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
