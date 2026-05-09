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


def find_char_by_id(player_id):

    for file in os.listdir(CHAR_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(CHAR_DIR, file)

        data = load_json(path)

        if not data:
            continue

        if str(data.get("id")) == str(player_id):
            return path, data

    return None, None


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

    try:

        for file in os.listdir(CHAR_DIR):

            if not file.endswith(".json"):
                continue

            path = os.path.join(CHAR_DIR, file)

            data = load_json(path)

            if not data:
                continue

            chars.append({
                "id": data.get("id"),
                "char": data.get("char")
            })

        return jsonify(chars), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# GET PLAYER DATA
# ----------------------------

@app.route("/get", methods=["GET"])
def get_data():

    web_id = request.args.get("id")
    web_token = request.args.get("token")

    if not all([web_id, web_token]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    try:

        _, data = find_char_by_id(web_id)

        if not data:
            return jsonify({"erro": "personagem nao encontrado"}), 404

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# SAVE FULL DATA
# ----------------------------

@app.route("/save", methods=["POST"])
def save_data():

    body = request.get_json()

    if not body:
        return jsonify({"erro": "body vazio"}), 400

    web_token = body.get("token")
    web_data = body.get("data")
    web_id = body.get("id")

    if not all([web_token, web_data, web_id]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    if not isinstance(web_data, dict):
        return jsonify({"erro": "data invalida"}), 400

    try:

        path, _ = find_char_by_id(web_id)

        if not path:
            return jsonify({"erro": "personagem nao encontrado"}), 404

        save_json(path, web_data)

        return jsonify({
            "msg": "salvo com sucesso"
        }), 200

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

    web_id = body.get("id")
    web_token = body.get("token")
    web_xp = body.get("xp")

    if not all([web_id, web_token, web_xp]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    try:
        web_xp = int(web_xp)

    except:
        return jsonify({"erro": "xp precisa ser numero"}), 400

    try:

        path, data = find_char_by_id(web_id)

        if not data:
            return jsonify({"erro": "personagem nao encontrado"}), 404

        data["xp"] = data.get("xp", 0) + web_xp

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

    web_id = body.get("id")
    web_token = body.get("token")
    web_newgeneration = body.get("newgeneration")

    if not all([web_id, web_token, web_newgeneration]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    try:
        web_newgeneration = int(web_newgeneration)

    except:
        return jsonify({"erro": "generation precisa ser numero"}), 400

    try:

        path, data = find_char_by_id(web_id)

        if not data:
            return jsonify({"erro": "personagem nao encontrado"}), 404

        data["generation"] = web_newgeneration

        save_json(path, data)

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# DELETE JSON
# ----------------------------

@app.route("/delete", methods=["DELETE"])
def delete_json():

    body = request.get_json()

    if not body:
        return jsonify({"erro": "body vazio"}), 400

    web_token = body.get("token")
    web_id = body.get("id")

    if not all([web_token, web_id]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    try:

        path, _ = find_char_by_id(web_id)

        if not path:
            return jsonify({"erro": "personagem nao encontrado"}), 404

        os.remove(path)

        return jsonify({
            "msg": "arquivo deletado"
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# UPLOAD JSON
# ----------------------------

@app.route("/upload", methods=["POST"])
def upload_json():

    web_token = request.form.get("token")
    web_id = request.form.get("id")

    if not all([web_token, web_id]):
        return jsonify({"erro": "faltando parametros"}), 400

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    file = request.files.get("file")

    if not file:
        return jsonify({"erro": "arquivo nao enviado"}), 400

    try:

        new_data = json.load(file)

    except:
        return jsonify({"erro": "json invalido"}), 400

    try:

        path, _ = find_char_by_id(web_id)

        if not path:
            return jsonify({"erro": "personagem nao encontrado"}), 404

        save_json(path, new_data)

        return jsonify({
            "msg": "upload concluido"
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# DOWNLOAD JSON
# ----------------------------

@app.route("/download/<player_id>", methods=["GET"])
def download_json(player_id):

    web_token = request.args.get("token")

    if not check_token(web_token):
        return jsonify({"erro": "token invalido"}), 401

    try:

        path, _ = find_char_by_id(player_id)

        if not path:
            return jsonify({"erro": "personagem nao encontrado"}), 404

        return send_file(
            path,
            as_attachment=True,
            download_name=f"{player_id}.json"
        )

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ----------------------------
# RUN SERVER
# ----------------------------

if __name__ == "__main__":
    app.run()