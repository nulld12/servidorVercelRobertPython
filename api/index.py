from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os


app = Flask(__name__)
CORS(app)
mongoUri= os.getenv("MONGO_URI","mongodb+srv://david:DavidNuria.22@clusterclase.xg533.mongodb.net/?retryWrites=true&w=majority&appName=ClusterClase")
cliente=MongoClient(mongoUri)
db= cliente.webVercelPython
users = db.usuarios


@app.route("/api")
def home():
    return "Hello, World!"




@app.route("/api/users", methods=["GET"])
def get_users():
    """
    Devuelve la lista entera de usuarios
    """
    try:
        listaUsuarios= users.find()
        listaUsuarios1=[]
        for user in listaUsuarios:
            if "_id" in user:
                user["_id"] = str(user["_id"])
            # Si manejas un campo 'id' con números
            if "id" in user and isinstance(user["id"], int):
                user["id"] = str(user["id"])
            listaUsuarios1.append(user)
        return jsonify(listaUsuarios1),200
    except Exception as e:
        return jsonify({'error': str(e)}),500        


@app.route("/api/users", methods=["POST"])
def add_users():
    """
    Agrega un nuevo usuario
    """
    data = request.get_json()

    # Validar que se haya proporcionado el cuerpo de la petición
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    # Extraer los campos
    user_id = data.get("id")
    nombre = data.get("nombre")
    telefono = data.get("telefono")
    edad = data.get("edad")
    
    required_fields = ["id", "nombre", "telefono", "edad"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido '{field}'"}), 400

    try:
        user_id = int(data["id"])
        edad = int(data["edad"])
    except ValueError:
        return jsonify({"error": "Los campos id y edad deben ser valores numéricos (enteros)"}), 400
    nombre = data["nombre"]
    telefono = data["telefono"]

    # Validar que nombre y teléfono son texto
    if not isinstance(nombre, str):
        return jsonify({"error": "El campo 'nombre' debe ser texto"}), 400
    if not isinstance(telefono, str):
        return jsonify({"error": "El campo 'telefono' debe ser texto"}), 400

    nuevoUsuario = {"id": user_id, "nombre": nombre, "telefono": telefono, "edad": edad}
    try:
        resultado= users.insert_one(nuevoUsuario)
        if "_id" in nuevoUsuario:
            nuevoUsuario["_id"] = str(nuevoUsuario["_id"])
        nuevoUsuario['id'] = str(resultado.inserted_id)
        return jsonify(nuevoUsuario), 201
    except Exception as e:
        print("ERROR en add_users:", e) 
        return jsonify({"error":str(e)}),500


@app.route("/api/oneUser/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """
    devuelve el usuario buscado por id
    """
    try:
        user = users.find_one({"id": user_id})
        if user:
            user['_id'] = str(user['_id'])
            user['id'] = str(user['id'])
            return jsonify(user), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error":str(e)}),500

