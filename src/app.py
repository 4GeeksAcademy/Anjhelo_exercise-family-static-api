"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()



    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def agregar_miembro():
    try:
        data = request.json
        first_name = data.get("first_name")
        age = data.get("age")
        numeros = data.get("lucky_numbers")

        if first_name is None or age is None or numeros is None:
            return jsonify({"error": "Faltan datos en la solicitud"}), 400

        status = jackson_family.add_member(first_name, age, numeros)

        if status.get("status") == 400:
            return jsonify({"error": status["error"]}), 400

        return jsonify(jackson_family.get_all_members()), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/member/<int:id>', methods=['DELETE'])
def eliminar_miembro(id):
    try:
        result = jackson_family.delete_member(id)
        if "done" in result:
            return jsonify(result), 200
        return jsonify(result), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

    
@app.route('/member/<int:member_id>', methods=['GET'])
def obtener_miembro(member_id):
    try:

        status = jackson_family.get_member(member_id)
        if status.get("status") == 400:
            return jsonify({"error": status["error"]}), 400
        return jsonify(status.get("miembro")), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
