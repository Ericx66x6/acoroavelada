from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# ----------------------------
# CONFIG
# ----------------------------

TOKEN = "acoroavelada2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_DIR = os.path.join(BASE_DIR, "..", "json")
CHAR_DIR = os.path.join(JSON_DIR, "characters")

GAME_FILE = os.path.join(JSON_DIR, "game_data.json")

os.makedirs(CHAR_DIR, exist_ok=True)


# ----------------------------
# HELPERS
# ----------------------------

def load_json(path):

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def check_token(web_token):
    return web_token == TOKEN


# ----------------------------
# HOME
# ----------------------------

@app.route("/")
def home():
    return "Servidor rodando!"


# ----------------------------
# GAME DATA GLOBAL
# ----------------------------

@app.route("/game", methods=["GET"])
def get_game():

    try:
        data = load_json(GAME_FILE)

        if data is None:
            return jsonify({"erro": "game_data nao encontrado"}), 404

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# LIST CHARS
# ----------------------------

@app.route("/listchars", methods=["GET"])
def list_chars():

    chars = []

    for file in os.listdir(CHAR_DIR):

        if file.endswith(".json") and os.path.isfile(os.path.join(CHAR_DIR, file)): 
            chars.append(file.replace(".json", ""))

    return jsonify(chars), 200


# ----------------------------
# GET PLAYER DATA
# ----------------------------

@app.route("/get", methods=["GET"])
def get_data():

    web_name = request.args.get("char")
    web_token = request.args.get("token")

    if not all([web_name, web_token]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    if not web_name.isalnum():
        return jsonify({"erro": "nome invalido"}), 400

    path = os.path.join(CHAR_DIR, f"{web_name}.json")

    data = load_json(path)

    if data is None:
        return jsonify({"erro": "personagem nao encontrado"}), 404

    return jsonify(data), 200


# ----------------------------
# SAVE FULL DATA
# ----------------------------

@app.route("/save", methods=["POST"])
def save_data():

    body = request.get_json()

    if not body:
        return jsonify({"erro": "body vazio"}), 400

    web_name = body.get("char")
    web_token = body.get("token")
    web_data = body.get("data")

    if not all([web_name, web_token, web_data]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    if not web_name.isalnum():
        return jsonify({"erro": "nome invalido"}), 400

    if not isinstance(web_data, dict):
        return jsonify({"erro": "data invalida"}), 400

    path = os.path.join(CHAR_DIR, f"{web_name}.json")

    try:
        save_json(path, web_data)
        return jsonify({"msg": "salvo com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# ADD XP
# ----------------------------

@app.route("/addxp", methods=["POST"])
def addxp():

    body = request.get_json()

    if not body:
        return jsonify({"erro": "body vazio"}), 400

    web_name = body.get("char")
    web_token = body.get("token")
    web_xp = body.get("xp")

    if not all([web_name, web_token, web_xp]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    try:
        web_xp = int(web_xp)

    except:
        return jsonify({"erro": "xp precisa ser numero"}), 400

    path = os.path.join(CHAR_DIR, f"{web_name}.json")

    data = load_json(path)

    if data is None:
        return jsonify({"erro": "personagem nao encontrado"}), 404

    data["xp"] = data.get("xp", 0) + web_xp

    try:
        save_json(path, data)
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# CHANGE GENERATION
# ----------------------------

@app.route("/changegeneration", methods=["POST"])
def change_generation():

    body = request.get_json()

    if not body:
        return jsonify({"erro": "body vazio"}), 400

    web_name = body.get("char")
    web_token = body.get("token")
    web_newgeneration = body.get("newgeneration")

    if not all([web_name, web_token, web_newgeneration]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    try:
        web_newgeneration = int(web_newgeneration)

    except:
        return jsonify({"erro": "generation precisa ser numero"}), 400

    path = os.path.join(CHAR_DIR, f"{web_name}.json")

    data = load_json(path)

    if data is None:
        return jsonify({"erro": "personagem nao encontrado"}), 404

    data["generation"] = web_newgeneration

    try:
        save_json(path, data)
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# DELETE JSON
# ----------------------------

@app.route("/delete/<name>", methods=["DELETE"])
def delete_json(name):

    body = request.get_json()

    if not body:
        return jsonify({"erro": "body vazio"}), 400

    web_token = body.get("token")

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    path = os.path.join(CHAR_DIR, f"{name}.json")

    if not os.path.exists(path):
        return jsonify({"erro": "arquivo nao encontrado"}), 404

    try:
        os.remove(path)
        return jsonify({"msg": "arquivo deletado"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# UPLOAD JSON
# ----------------------------

@app.route("/upload/<name>", methods=["POST"])
def upload_json(name):

    web_token = request.form.get("token")

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    file = request.files.get("file")

    if not file:
        return jsonify({"erro": "arquivo nao enviado"}), 400

    try:
        data = json.load(file)

    except:
        return jsonify({"erro": "json invalido"}), 400

    path = os.path.join(CHAR_DIR, f"{name}.json")

    try:
        save_json(path, data)
        return jsonify({"msg": "upload concluido"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# DOWNLOAD JSON
# ----------------------------

@app.route("/download/<name>", methods=["GET"])
def download_json(name):

    web_token = request.args.get("token")

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    path = os.path.join(CHAR_DIR, f"{name}.json")

    if not os.path.exists(path):
        return jsonify({"erro": "arquivo nao encontrado"}), 404

    return send_file(
        path,
        as_attachment=True,
        download_name=f"{name}.json"
    )


# ----------------------------
# RUN SERVER
# ----------------------------

if __name__ == "__main__":
    app.run()