# Painel Admin — A Coroa Velada
import requests
import os
import json

BASE_URL = "https://acoroavelada.onrender.com"
#BASE_URL = "http://localhost:5000"
ADMIN_TOKEN = "2755Eric!"


# =====================================
# UTIL
# =====================================


def pause():
    input("\nEnter para continuar...")


# =====================================
# PLAYER
# =====================================

def list_players():

    r = requests.get(
        f"{BASE_URL}/get/players",
        params={
            "token": ADMIN_TOKEN
        }
    )

    print(r.status_code)

    try:

        data = r.json()

        print("\n==============================")
        print("LISTA DE PLAYERS")
        print("==============================\n")

        for player in data:

            print(
                f'ID: {player["id"]} | '
                f'Player: {player["player"]} | '
                f'Char: {player["char"]}'
            )

    except Exception as e:

        print("Erro ao ler resposta:")
        print(e)
        print(r.text)

    pause()


def get_player():
    player_id = input("Player ID: ")

    r = requests.get(
        f"{BASE_URL}/get/player_data",
        params={
            "id": player_id,
            "token": ADMIN_TOKEN
        }
    )

    print(r.status_code)

    try:
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    except:
        print(r.text)

    pause()



def download_player():
    player_id = input("Player ID: ")

    r = requests.get(
        f"{BASE_URL}/download/player/{player_id}",
        params={
            "token": ADMIN_TOKEN
        }
    )

    print(r.status_code)

    if r.status_code == 200:

        filename = (
            r.headers["Content-Disposition"]
            .split("filename=")[1]
            .replace('"', "")
        )

        with open(filename, "wb") as f:
            f.write(r.content)

        print(f"Download concluído: {filename}")

    else:
        print(r.text)

    pause()



def upload_player():
    filepath = input("Caminho do JSON: ")

    if not os.path.exists(filepath):
        print("Arquivo não encontrado")
        pause()
        return

    with open(filepath, "rb") as f:

        files = {
            "file": f
        }

        data = {
            "token": ADMIN_TOKEN
        }

        r = requests.post(
            f"{BASE_URL}/upload/player",
            files=files,
            data=data
        )

    print(r.status_code)
    print(r.text)

    pause()



def delete_player():
    player_id = input("Player ID: ")

    confirm = input("Tem certeza? (y/n): ").lower()

    if confirm != "y":
        return

    r = requests.delete(
        f"{BASE_URL}/delete/player/{player_id}",
        params={
            "token": ADMIN_TOKEN
        }
    )

    print(r.status_code)
    print(r.text)

    pause()


# =====================================
# GAME DATA
# =====================================


def download_game():

    r = requests.get(
        f"{BASE_URL}/download/game",
        params={
            "token": ADMIN_TOKEN
        }
    )

    print(r.status_code)

    if r.status_code == 200:

        filename = (
            r.headers["Content-Disposition"]
            .split("filename=")[1]
            .replace('"', "")
        )

        with open(filename, "wb") as f:
            f.write(r.content)

        print(f"Download concluído: {filename}")

    else:
        print(r.text)

    pause()



def upload_game():
    filepath = input("Caminho do game_data.json: ")

    if not os.path.exists(filepath):
        print("Arquivo não encontrado")
        pause()
        return

    with open(filepath, "rb") as f:

        files = {
            "file": f
        }

        data = {
            "token": ADMIN_TOKEN
        }

        r = requests.post(
            f"{BASE_URL}/upload/game",
            files=files,
            data=data
        )

    print(r.status_code)
    print(r.text)

    pause()


# =====================================
# PROFILE PICTURE
# =====================================


def upload_profile_picture():
    filepath = input("Caminho da imagem: ")
    name = input("Nome final do arquivo: ")

    if not os.path.exists(filepath):
        print("Arquivo não encontrado")
        pause()
        return

    with open(filepath, "rb") as f:

        files = {
            "file": f
        }

        data = {
            "token": ADMIN_TOKEN,
            "name": name
        }

        r = requests.post(
            f"{BASE_URL}/upload/profile_picture",
            files=files,
            data=data
        )

    print(r.status_code)
    print(r.text)

    pause()


# =====================================
# UPDATE PLAYER
# =====================================


def update_stat():

    payload = {
        "player_id": int(input("Player ID: ")),
        "token": ADMIN_TOKEN,
        "action": "update_stat",
        "key": input("Key: "),
        "stat_id": int(input("Stat ID: ")),
        "value": int(input("Valor: "))
    }

    r = requests.post(
        f"{BASE_URL}/update/player",
        json=payload
    )

    print(r.status_code)

    try:
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    except:
        print(r.text)

    pause()



def add_xp():

    payload = {
        "player_id": int(input("Player ID: ")),
        "token": ADMIN_TOKEN,
        "action": "add_xp",
        "value": int(input("XP: ")),
        "stat_id": 0
    }

    r = requests.post(
        f"{BASE_URL}/update/player",
        json=payload
    )

    print(r.status_code)

    try:
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    except:
        print(r.text)

    pause()



def add_discipline():

    payload = {
        "player_id": int(input("Player ID: ")),
        "token": ADMIN_TOKEN,
        "action": "add_discipline",
        "stat_id": int(input("Discipline ID: ")),
        "value": int(input("Nível: "))
    }

    r = requests.post(
        f"{BASE_URL}/update/player",
        json=payload
    )

    print(r.status_code)

    try:
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    except:
        print(r.text)

    pause()



def add_ritual():

    payload = {
        "player_id": int(input("Player ID: ")),
        "token": ADMIN_TOKEN,
        "action": "add_ritual",
        "stat_id": int(input("Ritual ID: ")),
        "value": 0
    }

    r = requests.post(
        f"{BASE_URL}/update/player",
        json=payload
    )

    print(r.status_code)

    try:
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    except:
        print(r.text)

    pause()



def add_caracteristic():

    payload = {
        "player_id": int(input("Player ID: ")),
        "token": ADMIN_TOKEN,
        "action": "add_caracteristic",
        "stat_id": int(input("Caracteristic ID: ")),
        "value": 0
    }

    r = requests.post(
        f"{BASE_URL}/update/player",
        json=payload
    )

    print(r.status_code)

    try:
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    except:
        print(r.text)

    pause()



def update_morality():

    payload = {
        "player_id": int(input("Player ID: ")),
        "token": ADMIN_TOKEN,
        "action": "update_morality",
        "stat_id": int(input("Morality ID: ")),
        "description": input("Descrição: "),
        "value": 0
    }

    r = requests.post(
        f"{BASE_URL}/update/player",
        json=payload
    )

    print(r.status_code)

    try:
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    except:
        print(r.text)

    pause()


def give_session_xp():

    players = []

    amount = int(input("Quantidade de jogadores: "))
    xp = int(input("XP da sessão: "))

    for i in range(amount):

        player_id = int(input(f"Player ID #{i+1}: "))
        players.append(player_id)

    print("\nEnviando XP...\n")

    success = 0
    fail = 0

    for player_id in players:

        payload = {
            "player_id": player_id,
            "token": ADMIN_TOKEN,
            "action": "add_xp",
            "value": xp,
            "stat_id": 0
        }

        try:

            r = requests.post(
                f"{BASE_URL}/update/player",
                json=payload
            )

            if r.status_code == 200:
                print(f"[OK] Player {player_id}")
                success += 1

            else:
                print(f"[ERRO] Player {player_id}")
                print(r.text)
                fail += 1

        except Exception as e:
            print(f"[ERRO] Player {player_id}: {e}")
            fail += 1

    print("\n===================")
    print(f"Sucesso: {success}")
    print(f"Falhas: {fail}")
    print("===================\n")

    pause()

# =====================================
# MENU
# =====================================


while True:

    os.system("cls")

    print("""
==============================
A COROA VELADA - ADMIN PANEL
==============================
          
0  - List Players

1  - Get Player
2  - Download Player
3  - Upload Player
4  - Delete Player

5  - Download Game Data
6  - Upload Game Data

7  - Upload Profile Picture

8  - Update Stat
9  - Add XP
10 - Add Discipline
11 - Add Ritual
12 - Add Caracteristic
13 - Update Morality

14 - Give Session XP

0  - Sair
""")

    option = input("> ")

    if option == "0":
        list_players()

    elif option == "1":
        get_player()

    elif option == "2":
        download_player()

    elif option == "3":
        upload_player()

    elif option == "4":
        delete_player()

    elif option == "5":
        download_game()

    elif option == "6":
        upload_game()

    elif option == "7":
        upload_profile_picture()

    elif option == "8":
        update_stat()

    elif option == "9":
        add_xp()

    elif option == "10":
        add_discipline()

    elif option == "11":
        add_ritual()

    elif option == "12":
        add_caracteristic()

    elif option == "13":
        update_morality()

    elif option == "14":
        give_session_xp()

    elif option == "0":
        break

    else:
        print("Opção inválida")
        pause()
