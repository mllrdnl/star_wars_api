"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def people():
    people_query = People.query.all()
    response_body = [x.serialize() for x in people_query]
    #this is list comprehenshion, similar to map but simpler
    
    return jsonify(response_body), 200

@app.route('/people/<int:id>', methods=['GET'])
def people_by_id(id):
    people_query = People.query.filter(People.id == id).first()
    response_body = people_query.serialize()
    
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def planets():
    planets_query = Planets.query.all()
    response_body = [x.serialize() for x in planets_query]

    return jsonify(respons_body), 200

@app.route('/planets/<int:id>', methods=['GET'])
def planets_by_id(id):
    planets_query = Planets.query.filter(Planets.id == id).first()
    response_body = planets_query.serialize()
    

    return jsonify(response_body), 200

@app.route('/vehicles', methods=['GET'])
def vehicles():
    vehicles_query = Vehicles.query.all()
    response_body = [x.serialize() for x in vehicles_query]    

    return jsonify(response_body), 200

@app.route('/vehicles/<int:id>', methods=['GET'])
def vehicles_by_id(id):
    vehicles_query = Vehicles.query.filter(Vehicles.id == id).first()
    response_body = vehicles_query.serialize()
    
    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
