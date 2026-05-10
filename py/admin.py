import requests
import os

base_url = "https://acoroavelada.onrender.com"

# ----------------------------
# CONFIG
# ----------------------------

ADMIN_TOKEN = input("🔐 ADMIN TOKEN: ")

current_id = None  # 💡 mantém o último player usado


# ----------------------------
# UTIL
# ----------------------------

def pause():
    input("\nEnter para continuar...")


def auth():
    return ADMIN_TOKEN


def ask_id():
    global current_id

    use_last = input(f"Usar último ID ({current_id})? [s/n]: ")

    if use_last.lower() == "s" and current_id:
        return current_id

    current_id = input("ID do personagem: ")
    return current_id


def safe_request(r):
    try:
        data = r.json()
    except:
        data = {}

    if r.status_code == 200:
        print("\n✔ Sucesso")
        if "msg" in data:
            print("→", data["msg"])
    else:
        print(f"\n❌ Erro HTTP {r.status_code}")
        if "erro" in data:
            print("→", data["erro"])


# ----------------------------
# CORE REQUEST WRAPPER
# ----------------------------

def post(route, payload):
    return requests.post(base_url + route, json=payload)


def delete(route, payload):
    return requests.delete(base_url + route, json=payload)


# ----------------------------
# XP
# ----------------------------

def add_xp():
    pid = ask_id()
    xp = input("XP: ")

    r = post("/addxp", {
        "id": pid,
        "token": auth(),
        "xp": xp
    })

    safe_request(r)
    pause()


def xp_session():
    xp = input("XP da sessão: ")

    print("\nIDs (0 pra finalizar)")
    ids = []

    while True:
        i = input("> ")
        if i == "0":
            break
        if i.strip():
            ids.append(i)

    for pid in ids:
        r = post("/addxp", {
            "id": pid,
            "token": auth(),
            "xp": xp
        })
        print(f"{pid}: {r.status_code}")

    pause()


# ----------------------------
# GEN / DELETE
# ----------------------------

def change_gen():
    pid = ask_id()
    gen = input("Nova geração: ")

    r = post("/changegeneration", {
        "id": pid,
        "token": auth(),
        "newgeneration": gen
    })

    safe_request(r)
    pause()


def delete_char():
    pid = ask_id()

    confirm = input("Tem certeza? (s/n): ")
    if confirm.lower() != "s":
        print("Cancelado.")
        return

    r = delete("/delete", {
        "id": pid,
        "token": auth()
    })

    safe_request(r)
    pause()


# ----------------------------
# UPDATE SYSTEMS
# ----------------------------

def add_ritual():
    pid = ask_id()
    rid = input("Ritual ID: ")

    r = post("/addritual", {
        "id": pid,
        "token": auth(),
        "ritual": rid
    })

    safe_request(r)
    pause()


def add_discipline():
    pid = ask_id()
    did = input("Disciplina ID: ")
    lvl = input("Nível: ")

    r = post("/adddiscipline", {
        "id": pid,
        "token": auth(),
        "discipline_id": did,
        "nivel": lvl
    })

    safe_request(r)
    pause()


def update_stat():
    pid = ask_id()

    print("\natributes / knowledges / expertises / talents")
    cat = input("Categoria: ")

    sid = input("Stat ID: ")
    val = input("Valor: ")

    r = post("/updatestats", {
        "id": pid,
        "token": auth(),
        "category": cat,
        "id_stat": sid,
        "value": val
    })

    safe_request(r)
    pause()


def update_morality():
    pid = ask_id()

    mid = input("Morality ID: ")
    desc = input("Descrição: ")

    r = post("/updatemorality", {
        "id": pid,
        "token": auth(),
        "id_morality": mid,
        "description": desc
    })

    safe_request(r)
    pause()


def add_characteristic():
    pid = ask_id()
    cid = input("Characteristic ID: ")

    r = post("/addcharacteristic", {
        "id": pid,
        "token": auth(),
        "characteristic_id": cid
    })

    safe_request(r)
    pause()


# ----------------------------
# LIST
# ----------------------------

def list_chars():
    r = requests.get(base_url + "/listchars")

    if r.status_code != 200:
        print("Erro")
        pause()
        return

    print("\n=== PERSONAGENS ===")

    for c in r.json():
        print(f'{c["id"]} | {c["char"]}')

    pause()


# ----------------------------
# MENU
# ----------------------------

def menu():
    print("""
========================
 RPG ADMIN PANEL
========================
1  XP player
2  XP sessão
3  mudar geração
4  listar chars
5  deletar char
6  ritual
7  disciplina
8  stats
9  moralidade
10 característica
0  sair
========================
""")


# ----------------------------
# LOOP
# ----------------------------

while True:
    menu()
    op = input("→ ")

    if op == "1": add_xp()
    elif op == "2": xp_session()
    elif op == "3": change_gen()
    elif op == "4": list_chars()
    elif op == "5": delete_char()
    elif op == "6": add_ritual()
    elif op == "7": add_discipline()
    elif op == "8": update_stat()
    elif op == "9": update_morality()
    elif op == "10": add_characteristic()
    elif op == "0": break
    else: print("inválido")