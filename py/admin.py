import requests
import os
import json

base_url = "http://127.0.0.1:5000"


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

    else:

        print(f"\n❌ Erro HTTP {r.status_code}")

        if "erro" in data:
            print(data["erro"])


# ----------------------------
# TOKEN
# ----------------------------

def ask_token():
    return input("Token: ")


# ----------------------------
# DAR XP
# ----------------------------

def send_xp():

    char = input("Personagem: ")
    token = ask_token()
    xp = input("XP: ")

    payload = {
        "char": char,
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

    print("\nDigite os personagens que vão receber XP")
    print("Digite '0' para finalizar\n")

    chars = []

    while True:

        char = input("Personagem: ")

        if char == "0":
            break

        if char.strip() == "":
            continue

        chars.append(char)

    if len(chars) == 0:
        print("❌ Nenhum personagem informado")
        pause()
        return

    print("\n========================")
    print("       XP SESSÃO")
    print("========================")

    for char in chars:

        payload = {
            "char": char,
            "token": token,
            "xp": xp
        }

        r = requests.post(base_url + "/addxp", json=payload)

        if r.status_code == 200:
            print(f"✔ {char} +{xp} XP")

        else:
            try:
                print(f"❌ {char}: {r.json().get('erro')}")

            except:
                print(f"❌ {char}: erro desconhecido")

    pause()


# ----------------------------
# MUDAR GERAÇÃO
# ----------------------------

def change_generation():

    char = input("Personagem: ")
    token = ask_token()
    gen = input("Nova geração: ")

    payload = {
        "char": char,
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
        print("-", char)

    pause()


# ----------------------------
# DOWNLOAD JSON
# ----------------------------

def download_char():

    char = input("Personagem: ")
    token = ask_token()

    r = requests.get(
        f"{base_url}/download/{char}",
        params={"token": token}
    )

    if r.status_code != 200:
        safe_request(r)
        pause()
        return

    filename = f"{char}.json"

    with open(filename, "wb") as f:
        f.write(r.content)

    print(f"\n✔ Arquivo salvo como {filename}")

    pause()


# ----------------------------
# UPLOAD JSON
# ----------------------------

def upload_char():

    path = input("Caminho do JSON: ")
    name = input("Nome do personagem: ")
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
                "token": token
            }

            r = requests.post(
                f"{base_url}/upload/{name}",
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

    char = input("Personagem: ")
    token = ask_token()

    confirm = input(f'Tem certeza que deseja deletar "{char}"? (s/n): ')

    if confirm.lower() != "s":
        print("Cancelado.")
        pause()
        return

    payload = {
        "token": token
    }

    r = requests.delete(
        f"{base_url}/delete/{char}",
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