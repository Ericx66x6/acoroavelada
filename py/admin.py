import requests
import os
import json

base_url = "https://acoroavelada.onrender.com"


# ----------------------------
# UTIL
# ----------------------------

def pause():
    input("\nEnter para voltar...")


def safe_request(r):

    try:
        data = r.json()

    except:
        data = {}

    if r.status_code == 200:

        print("\n✔ Sucesso")

        if isinstance(data, dict):

            if "msg" in data:
                print(data["msg"])

    else:

        print(f"\n❌ Erro HTTP {r.status_code}")

        if "erro" in data:
            print(data["erro"])


def find_char_by_id(player_id):

    r = requests.get(base_url + "/listchars")

    if r.status_code != 200:
        return None

    chars = r.json()

    for char in chars:

        if str(char.get("id")) == str(player_id):
            return char

    return None


# ----------------------------
# TOKEN
# ----------------------------

def ask_token():
    return input("Token: ")


def ask_player_id():
    return input("ID do personagem: ")


# ----------------------------
# DAR XP
# ----------------------------

def send_xp():

    player_id = ask_player_id()
    token = ask_token()
    xp = input("XP: ")

    payload = {
        "id": player_id,
        "token": token,
        "xp": xp
    }

    r = requests.post(base_url + "/addxp", json=payload)

    safe_request(r)
    pause()


# ----------------------------
# XP DA SESSÃO
# ----------------------------

def send_xp_session():

    token = ask_token()
    xp = input("XP para os jogadores: ")

    print("\nDigite os IDs dos personagens")
    print("Digite '0' para finalizar\n")

    ids = []

    while True:

        player_id = input("ID: ")

        if player_id == "0":
            break

        if player_id.strip() == "":
            continue

        ids.append(player_id)

    if len(ids) == 0:
        print("❌ Nenhum personagem informado")
        pause()
        return

    print("\n========================")
    print("       XP SESSÃO")
    print("========================")

    for player_id in ids:

        payload = {
            "id": player_id,
            "token": token,
            "xp": xp
        }

        r = requests.post(base_url + "/addxp", json=payload)

        if r.status_code == 200:

            char = find_char_by_id(player_id)

            if char:
                print(f'✔ {char.get("char")} +{xp} XP')

            else:
                print(f'✔ ID {player_id} +{xp} XP')

        else:

            try:
                print(f"❌ ID {player_id}: {r.json().get('erro')}")

            except:
                print(f"❌ ID {player_id}: erro desconhecido")

    pause()


# ----------------------------
# MUDAR GERAÇÃO
# ----------------------------

def change_generation():

    player_id = ask_player_id()
    token = ask_token()
    gen = input("Nova geração: ")

    payload = {
        "id": player_id,
        "token": token,
        "newgeneration": gen
    }

    r = requests.post(base_url + "/changegeneration", json=payload)

    safe_request(r)
    pause()


# ----------------------------
# LISTAR PERSONAGENS
# ----------------------------

def list_chars():

    r = requests.get(base_url + "/listchars")

    if r.status_code != 200:
        print("❌ Erro ao buscar personagens")
        pause()
        return

    chars = r.json()

    print("\n========================")
    print("     PERSONAGENS")
    print("========================")

    for char in chars:

        print(
            f'ID: {char.get("id")} | '
            f'Nome: {char.get("char")}'
        )

    pause()


# ----------------------------
# DOWNLOAD JSON
# ----------------------------

def download_char():

    player_id = ask_player_id()
    token = ask_token()

    r = requests.get(
        f"{base_url}/download/{player_id}",
        params={"token": token}
    )

    if r.status_code != 200:
        safe_request(r)
        pause()
        return

    filename = f"{player_id}.json"

    with open(filename, "wb") as f:
        f.write(r.content)

    print(f"\n✔ Arquivo salvo como {filename}")

    pause()


# ----------------------------
# UPLOAD JSON
# ----------------------------

def upload_char():

    path = input("Caminho do JSON: ")
    player_id = ask_player_id()
    token = ask_token()

    if not path.endswith(".json"):
        print("❌ Arquivo precisa ser .json")
        pause()
        return

    try:

        with open(path, "rb") as f:

            files = {
                "file": f
            }

            data = {
                "token": token,
                "id": player_id
            }

            r = requests.post(
                f"{base_url}/upload",
                files=files,
                data=data
            )

    except Exception as e:

        print("❌ Erro ao abrir arquivo:")
        print(e)

        pause()
        return

    safe_request(r)
    pause()


# ----------------------------
# DOWNLOAD GAME DATA
# ----------------------------

def download_game_data():

    path = "./json/game_data.json"

    if not os.path.exists(path):
        print("❌ game_data.json não encontrado")
        pause()
        return

    try:

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        filename = "game_data.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"\n✔ Arquivo salvo como {filename}")

    except Exception as e:

        print("❌ Erro:")
        print(e)

    pause()


# ----------------------------
# UPLOAD GAME DATA
# ----------------------------

def upload_game_data():

    path = input("Caminho do JSON: ")

    if not os.path.exists(path):
        print("❌ Arquivo não encontrado")
        pause()
        return

    try:

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        with open("./json/game_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("\n✔ game_data.json atualizado")

    except Exception as e:

        print("❌ Erro:")
        print(e)

    pause()


# ----------------------------
# DELETAR PERSONAGEM
# ----------------------------

def delete_char():

    player_id = ask_player_id()
    token = ask_token()

    char = find_char_by_id(player_id)

    if char:
        confirm = input(
            f'Tem certeza que deseja deletar "{char.get("char")}"? (s/n): '
        )

    else:
        confirm = input(
            f'Tem certeza que deseja deletar ID "{player_id}"? (s/n): '
        )

    if confirm.lower() != "s":
        print("Cancelado.")
        pause()
        return

    payload = {
        "token": token,
        "id": player_id
    }

    r = requests.delete(
        f"{base_url}/delete",
        json=payload
    )

    safe_request(r)
    pause()


# ----------------------------
# MENU
# ----------------------------

def menu():

    print("\n========================")
    print("    RPG ADMIN CONSOLE")
    print("========================")
    print("1  - Dar XP")
    print("2  - Mudar geração")
    print("3  - Dar XP da sessão")
    print("4  - Listar personagens")
    print("5  - Download JSON")
    print("6  - Upload JSON")
    print("7  - Deletar personagem")
    print("8  - Download GameData")
    print("9  - Upload GameData")
    print("0  - Sair")
    print("========================")


# ----------------------------
# LOOP PRINCIPAL
# ----------------------------

while True:

    menu()

    choice = input("Escolha: ")

    if choice == "1":
        send_xp()

    elif choice == "2":
        change_generation()

    elif choice == "3":
        send_xp_session()

    elif choice == "4":
        list_chars()

    elif choice == "5":
        download_char()

    elif choice == "6":
        upload_char()

    elif choice == "7":
        delete_char()

    elif choice == "8":
        download_game_data()

    elif choice == "9":
        upload_game_data()

    elif choice == "0":
        print("Saindo...")
        break

    else:
        print("❌ Opção inválida")