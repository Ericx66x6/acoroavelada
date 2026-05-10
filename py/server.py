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

# 🔐 ADMIN TOKEN (usa isso no console/admin tools)
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


def sanitize(data):
    d = data.copy()
    d.pop("token", None)
    return d


def find_char_by_id(player_id):
    for file in os.listdir(CHAR_DIR):
        if not file.endswith(".json"):
            continue

        path = os.path.join(CHAR_DIR, file)
        data = load_json(path)

        if str(data.get("id")) == str(player_id):
            return path, data

    return None, None


def auth(player_data, player_token, admin_token):
    # admin ignora token do player
    if admin_token == ADMIN_TOKEN:
        return True

    return player_data and player_data.get("token") == player_token


def get_body():
    return request.get_json() or {}


def fail(msg, code=400):
    return jsonify({"erro": msg}), code


def ok(msg="ok"):
    return jsonify({"msg": msg}), 200


def update_player(player_id, player_token, admin_token, updater):
    path, data = find_char_by_id(player_id)

    if not data:
        return None, ("personagem nao encontrado", 404)

    if not auth(data, player_token, admin_token):
        return None, ("token invalido", 401)

    updater(data)
    save_json(path, data)

    return data, None


# ----------------------------
# GET PLAYER
# ----------------------------

@app.route("/get", methods=["GET"])
def get_player():
    player_id = request.args.get("id")
    token = request.args.get("token")

    if not player_id:
        return fail("faltando id")

    _, data = find_char_by_id(player_id)

    if not data:
        return fail("nao encontrado", 404)

    if token and not auth(data, token, ""):
        return fail("token invalido", 401)

    return jsonify(sanitize(data)), 200


# ----------------------------
# XP
# ----------------------------

@app.route("/addxp", methods=["POST"])
def add_xp():
    body = get_body()

    player_id = body.get("id")
    player_token = body.get("token")
    admin_token = body.get("admin_token")
    xp = body.get("xp")

    if None in [player_id, xp]:
        return fail("faltando parametros")

    try:
        xp = int(xp)
    except:
        return fail("xp invalido")

    def updater(d):
        d["xp"] = d.get("xp", 0) + xp

    _, err = update_player(player_id, player_token, admin_token, updater)
    if err:
        return fail(err[0], err[1])

    return ok("xp atualizado")


# ----------------------------
# MONEY
# ----------------------------

@app.route("/addmoney", methods=["POST"])
def add_money():
    body = get_body()

    player_id = body.get("id")
    admin_token = body.get("admin_token")
    amount = body.get("amount", 0)

    try:
        amount = int(amount)
    except:
        return fail("valor invalido")

    def updater(d):
        d["money"] = d.get("money", 0) + amount

    _, err = update_player(player_id, "", admin_token, updater)
    if err:
        return fail(err[0], err[1])

    return ok("money atualizado")


# ----------------------------
# ITEMS
# ----------------------------

@app.route("/additem", methods=["POST"])
def add_item():
    body = get_body()

    player_id = body.get("id")
    admin_token = body.get("admin_token")
    item = body.get("item")

    if not item:
        return fail("item faltando")

    def updater(d):
        if "items" not in d:
            d["items"] = []

        d["items"].append(item)

    _, err = update_player(player_id, "", admin_token, updater)
    if err:
        return fail(err[0], err[1])

    return ok("item adicionado")


# ----------------------------
# DISCIPLINE
# ----------------------------

@app.route("/adddiscipline", methods=["POST"])
def add_discipline():
    body = get_body()

    player_id = body.get("id")
    admin_token = body.get("admin_token")
    disc_id = body.get("discipline_id")
    nivel = int(body.get("nivel", 1))

    def updater(d):
        if "disciplines" not in d:
            d["disciplines"] = []

        found = next((x for x in d["disciplines"] if x["id"] == disc_id), None)

        if found:
            found["nivel"] = max(found["nivel"], nivel)
        else:
            d["disciplines"].append({"id": disc_id, "nivel": nivel})

    _, err = update_player(player_id, "", admin_token, updater)
    if err:
        return fail(err[0], err[1])

    return ok("disciplina atualizada")


# ----------------------------
# RITUAL
# ----------------------------

@app.route("/addritual", methods=["POST"])
def add_ritual():
    body = get_body()

    player_id = body.get("id")
    admin_token = body.get("admin_token")
    ritual_id = body.get("ritual")

    def updater(d):
        if "rituals" not in d:
            d["rituals"] = []

        if ritual_id not in [r.get("id") for r in d["rituals"]]:
            d["rituals"].append({"id": ritual_id})

    _, err = update_player(player_id, "", admin_token, updater)
    if err:
        return fail(err[0], err[1])

    return ok("ritual adicionado")


# ----------------------------
# CHARACTERISTIC
# ----------------------------

@app.route("/addcharacteristic", methods=["POST"])
def add_characteristic():
    body = get_body()

    player_id = body.get("id")
    admin_token = body.get("admin_token")
    char_id = body.get("characteristic_id")

    def updater(d):
        if "caracteristics" not in d:
            d["caracteristics"] = []

        if char_id not in [c.get("id") for c in d["caracteristics"]]:
            d["caracteristics"].append({"id": char_id})

    _, err = update_player(player_id, "", admin_token, updater)
    if err:
        return fail(err[0], err[1])

    return ok("characteristic adicionada")


# ----------------------------
# STATS GENERIC
# ----------------------------

@app.route("/updatestats", methods=["POST"])
def update_stats():
    body = get_body()

    player_id = body.get("id")
    admin_token = body.get("admin_token")
    category = body.get("category")
    stat_id = body.get("id_stat")
    value = body.get("value")

    allowed = ["atributes", "knowledges", "expertises", "talents"]

    if category not in allowed:
        return fail("categoria invalida")

    def updater(d):
        if category not in d:
            d[category] = []

        arr = d[category]

        found = next((x for x in arr if x["id"] == stat_id), None)

        if found:
            found["value"] = value
        else:
            arr.append({"id": stat_id, "value": value})

    _, err = update_player(player_id, "", admin_token, updater)
    if err:
        return fail(err[0], err[1])

    return ok("stats atualizados")


# ----------------------------
# RUN
# ----------------------------

if __name__ == "__main__":
    print("SERVER RUNNING...")
    app.run(debug=True)