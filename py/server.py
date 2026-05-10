from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "..", "json")
CHAR_DIR = os.path.join(JSON_DIR, "characters")

os.makedirs(CHAR_DIR, exist_ok=True)

ADMIN_TOKEN = "2755eric"


# ----------------------------
# HELPERS
# ----------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def find_char_by_id(player_id):
    for file in os.listdir(CHAR_DIR):
        if not file.endswith(".json"):
            continue

        path = os.path.join(CHAR_DIR, file)
        data = load_json(path)

        if str(data.get("id")) == str(player_id):
            return path, data

    return None, None


def is_admin(token):
    return token == ADMIN_TOKEN


def auth(data, player_token, admin_token):
    # admin SEMPRE passa
    if is_admin(admin_token) or is_admin(player_token):
        return True

    return data and data.get("token") == player_token


def update_player(pid, player_token, admin_token, updater):
    path, data = find_char_by_id(pid)

    if not data:
        return None, ("personagem nao encontrado", 404)

    if not auth(data, player_token, admin_token):
        return None, ("token invalido", 401)

    updater(data)
    save_json(path, data)

    return data, None


# ----------------------------
# XP (FIX DO SEU BUG)
# ----------------------------

@app.route("/addxp", methods=["POST"])
def add_xp():
    body = request.get_json()

    pid = body.get("id")
    xp = body.get("xp")

    # aceita os DOIS nomes sem quebrar client antigo
    token = body.get("token") or body.get("admin_token")

    if pid is None or xp is None:
        return jsonify({"erro": "faltando parametros"}), 400

    xp = int(xp)

    def updater(d):
        d["xp"] = d.get("xp", 0) + xp

    _, err = update_player(pid, token, token, updater)

    if err:
        return jsonify({"erro": err[0]}), err[1]

    return jsonify({"msg": "xp atualizado"}), 200


# ----------------------------
# MONEY
# ----------------------------

@app.route("/addmoney", methods=["POST"])
def add_money():
    body = request.get_json()

    pid = body.get("id")
    amount = int(body.get("amount", 0))
    token = body.get("token") or body.get("admin_token")

    def updater(d):
        d["money"] = d.get("money", 0) + amount

    _, err = update_player(pid, token, token, updater)

    if err:
        return jsonify({"erro": err[0]}), err[1]

    return jsonify({"msg": "money atualizado"}), 200


# ----------------------------
# DISCIPLINE
# ----------------------------

@app.route("/adddiscipline", methods=["POST"])
def add_discipline():
    body = request.get_json()

    pid = body.get("id")
    disc_id = body.get("discipline_id")
    nivel = int(body.get("nivel", 1))
    token = body.get("token") or body.get("admin_token")

    def updater(d):
        if "disciplines" not in d:
            d["disciplines"] = []

        found = next((x for x in d["disciplines"] if x["id"] == disc_id), None)

        if found:
            found["nivel"] = max(found["nivel"], nivel)
        else:
            d["disciplines"].append({"id": disc_id, "nivel": nivel})

    _, err = update_player(pid, token, token, updater)

    if err:
        return jsonify({"erro": err[0]}), err[1]

    return jsonify({"msg": "disciplina ok"}), 200


# ----------------------------
# RITUAL
# ----------------------------

@app.route("/addritual", methods=["POST"])
def add_ritual():
    body = request.get_json()

    pid = body.get("id")
    ritual_id = body.get("ritual")
    token = body.get("token") or body.get("admin_token")

    def updater(d):
        if "rituals" not in d:
            d["rituals"] = []

        if ritual_id not in [r.get("id") for r in d["rituals"]]:
            d["rituals"].append({"id": ritual_id})

    _, err = update_player(pid, token, token, updater)

    if err:
        return jsonify({"erro": err[0]}), err[1]

    return jsonify({"msg": "ritual ok"}), 200


# ----------------------------
# CHARACTERISTICS
# ----------------------------

@app.route("/addcharacteristic", methods=["POST"])
def add_characteristic():
    body = request.get_json()

    pid = body.get("id")
    cid = body.get("characteristic_id")
    token = body.get("token") or body.get("admin_token")

    def updater(d):
        if "caracteristics" not in d:
            d["caracteristics"] = []

        if cid not in [c.get("id") for c in d["caracteristics"]]:
            d["caracteristics"].append({"id": cid})

    _, err = update_player(pid, token, token, updater)

    if err:
        return jsonify({"erro": err[0]}), err[1]

    return jsonify({"msg": "characteristic ok"}), 200


# ----------------------------
# RUN
# ----------------------------

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    print("SERVER ONLINE 🔥")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
    print("SERVER READY 🔥 (compatível com client antigo)")
    app.run(debug=True)