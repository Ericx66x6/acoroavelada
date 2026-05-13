from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

ADMIN_TOKEN = "2755Eric!"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHAR_PATH = os.path.join(BASE_DIR, "json", "characters")
GAME_PATH = os.path.join(BASE_DIR, "json")

def find_player_by_id(player_id):
    for filename in os.listdir(CHAR_PATH):

        if not filename.endswith(".json"):
            continue

        path = os.path.join(CHAR_PATH, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                player_data = json.load(f)

            if str(player_data.get("id")) == str(player_id):
                return player_data, path

        except Exception as e:
            print(f"Erro ao ler {filename}: {e}")

    return None, None

@app.route("/", methods=["GET"])
def main():
    return "Servidor Online!"

@app.route("/get/game_data", methods=["GET"])
def get_game_data():
    path = os.path.join(GAME_PATH, "game_data.json")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            game_data = json.load(f)  
            print("Game Get Sucefully")          
            return game_data

    except Exception as e:
        return f"Erro ao obter o Game_Data: {e}"

@app.route("/get/player_data", methods=["GET"])
def get_player_data():
    url_player_id = request.args.get("id")
    url_token = request.args.get("token")

    if not url_player_id or not url_token:
        return jsonify({"error": "missing id or token"}), 400

    player_data, original_file_path = find_player_by_id(url_player_id)

    if not player_data:
        return jsonify({"error": "player not found"}), 404

    if player_data.get("token") != url_token and ADMIN_TOKEN != url_token:
        return jsonify({"error": "invalid token"}), 403

    print("Player Get Sucefully")
    return jsonify(player_data)


@app.route("/save/player_data", methods=["POST"])
def save_player():
    data = request.json

    url_player_id = data.get("id")
    url_token = data.get("token")
    url_player_data = data.get("data")

    if not url_player_id or not url_token or not url_player_data:
        return jsonify({"error": "missing data"}), 400

    player_data, original_file_path = find_player_by_id(url_player_id)

    if not player_data:
        return jsonify({"error": "player not found"}), 404

    if player_data.get("token") != url_token and ADMIN_TOKEN != url_token:
        return jsonify({"error": "invalid token"}), 403
    
    with open(original_file_path, "w", encoding="utf-8") as f:
        json.dump(url_player_data, f, indent=4, ensure_ascii=False)

    print ("Salvo com Sucesso !")
    return jsonify({"status": "saved"})

@app.route("/download/player/<int:player_id>")
def download_player(player_id):
    url_token = request.args.get("token")

    player_data,path = find_player_by_id(player_id)

    if not player_data:
        return jsonify({"error": "player not found"}), 404

    if ADMIN_TOKEN != url_token:
        return jsonify({"error": "invalid token"}), 403

    print("PATH:", path)
    print("EXISTS:", os.path.exists(path))

    return send_file(
        os.path.abspath(path),
        as_attachment=True
    )

@app.route("/upload/player", methods=["POST"])
def upload_player():
    url_token = request.form.get("token")

    if url_token != ADMIN_TOKEN:
        return jsonify({"error": "invalid token"}), 403

    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files["file"]

    save_path = os.path.join(CHAR_PATH, file.filename)

    file.save(save_path)

    return jsonify({"status": "uploaded"})

@app.route("/delete/player/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):

    url_token = request.args.get("token")

    player_data, original_file_path = find_player_by_id(player_id)

    if not player_data:
        return jsonify({"error": "player not found"}), 404

    if url_token != ADMIN_TOKEN:
        return jsonify({"error": "invalid token"}), 403

    os.remove(original_file_path)

    return jsonify({"status": "deleted"})

@app.route("/download/game", methods=["GET"])
def download_game():

    url_token = request.args.get("token")

    if url_token != ADMIN_TOKEN:
        return jsonify({"error": "invalid token"}), 403

    game_path = "./json/game_data.json"

    print("PATH:", game_path)
    print("EXISTS:", os.path.exists(game_path))

    return send_file(
        os.path.abspath(game_path),
        as_attachment=True
    )


@app.route("/upload/game", methods=["POST"])
def upload_game():

    url_token = request.form.get("token")

    if url_token != ADMIN_TOKEN:
        return jsonify({"error": "invalid token"}), 403

    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files["file"]

    game_path = "./json/game_data.json"

    file.save(game_path)

    return jsonify({"status": "uploaded"})

@app.route("/upload/profile_picture", methods=["POST"])
def upload_profile_picture():

    url_token = request.form.get("token")
    
    if url_token != ADMIN_TOKEN:
        return jsonify({"error": "invalid token"}), 403

    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files["file"]

    name = request.form.get("name")

    if not name:
        return jsonify({"error": "missing name"}), 400

    name = os.path.basename(name)

    print("FILE:", file)
    print("NAME:", name)
    print("__FILE__:", __file__)
    print("BASE_DIR:", BASE_DIR)

    img_dir = os.path.join(BASE_DIR, "img", "characters")

    print("IMG_DIR:", img_dir)

    os.makedirs(img_dir, exist_ok=True)

    img_path = os.path.join(img_dir, name)

    print("FINAL PATH:", img_path)

    file.save(img_path)

    print("EXISTS AFTER SAVE:", os.path.exists(img_path))

    return jsonify({
        "status": "uploaded",
        "path": img_path,
        "exists": os.path.exists(img_path)
    })

@app.route("/update/player", methods=["POST"])
def update_player():
    data = request.json

    url_player_id = int(data.get("player_id"))
    url_token = data.get("token")
    url_action = data.get("action")
    url_value = int(data.get("value"))
    url_key = data.get("key")
    url_stat_id = int(data.get("stat_id"))
    url_description = data.get("description")

    player_data, original_file_path = find_player_by_id(url_player_id)

    if not player_data:
        return jsonify({"error": "player not found"}), 404

    if ADMIN_TOKEN != url_token:
        return jsonify({"error": "invalid token"}), 403

    def update_morality(player_data, stat_id, description):
        for morality in player_data["moralityes"]:
            if int(morality["id"]) == stat_id:
                morality["description"] = description
                return True
            
        return False

    def update_stat(player_data, key, stat_id, value):
        valid_keys = [
            "atributes",
            "knowledges",
            "precedents",
            "expertises",
            "talents"
        ]

        if key not in valid_keys:
            return False

        for item in player_data[key]:
            if int(item["id"]) == stat_id:
                item["value"] += value
                return True

        return False

    def add_xp(player_data, value):
        xp = int(player_data.get("xp"))

        if xp + value < 0:
            return False

        player_data["xp"] = xp + value
        return True

    def add_discipline(player_data, stat_id, value):
        for discipline in player_data["disciplines"]:
            if int(discipline["id"]) == stat_id:
                player_data["disciplines"].remove(discipline)
                return True
            
        player_data["disciplines"].append({
            "id": int(stat_id),
            "nivel": int(value),
        })
        return True

    def add_ritual(player_data, stat_id):
        for ritual in player_data["rituals"]:
            if int(ritual["id"]) == stat_id:
                player_data["rituals"].remove(ritual)
                return True
            
        player_data["rituals"].append({
            "id": int(stat_id)
        })
        return True

    def add_caracteristic(player_data, stat_id):
        for caracteristic in player_data["caracteristics"]:
            if int(caracteristic["id"]) == stat_id:
                player_data["caracteristics"].remove(caracteristic)
                return True
            
        player_data["caracteristics"].append({
            "id": int(stat_id)
        })
        return True

    if url_action == "update_stat":
        update_stat(player_data, url_key, url_stat_id, url_value)

    elif url_action == "add_xp":
        add_xp(player_data, url_value)

    elif url_action == "add_discipline":
        add_discipline(player_data, url_stat_id, url_value)

    elif url_action == "add_ritual":
        add_ritual(player_data, url_stat_id)
    
    elif url_action == "add_caracteristic":
        add_caracteristic(player_data, url_stat_id)

    elif url_action == "update_morality":
        update_morality(player_data, url_stat_id, url_description)

    else:
        return jsonify({"error": "invalid action"}), 400

    with open(original_file_path, "w", encoding="utf-8") as f:
        json.dump(player_data, f, indent=4, ensure_ascii=False)

    return jsonify({"status": "ok", "player": player_data})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)