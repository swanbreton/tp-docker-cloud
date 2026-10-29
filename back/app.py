import os
import signal
import sys
import random
import json
import logging
import socket
from flask import Flask, jsonify, request
from flask_cors import CORS
from game_data import (
    CLASSES_STATS, SKILL_TREES, WEAPONS_BY_TIER,
    ARMORS_BY_TIER, MONSTERS_POOL, BOSSES_POOL, CONSUMABLES
)

app = Flask(__name__)
CORS(app)

signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))

PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
DATA_DIR = os.getenv("DATA_DIR", "/app/data")
LOG_DIR = os.getenv("LOG_DIR", "/app/logs")
GAME_SERVER_HOST = os.getenv("GAME_SERVER_HOST", "game-server")
GAME_SERVER_PORT = int(os.getenv("GAME_SERVER_PORT", "9000"))

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "backend.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("backend")
logger.info(f"Démarrage Backend Flask (Data: {DATA_DIR}, Logs: {LOG_DIR})")

ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
SAVE_FILE = os.path.join(DATA_DIR, "player_save.json")


def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur chargement comptes : {e}")
            return {}
    return {}


def save_accounts():
    try:
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump(accounts, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Erreur écriture comptes : {e}")


accounts = load_accounts()
player = None
current_user = None
current_event = None
current_monster = None
current_merchant_stock = []


def persist_save():
    global player, current_user, accounts
    if player:
        if current_user:
            if current_user not in accounts:
                accounts[current_user] = {"password": "", "high_score": 0, "level": 1, "class": ""}
            accounts[current_user]["high_score"] = max(accounts[current_user].get("high_score", 0), player["rooms_cleared"])
            accounts[current_user]["level"] = player["level"]
            accounts[current_user]["class"] = player["class_name"]
            save_accounts()

        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump({"user": current_user, "player": player}, f, indent=2, ensure_ascii=False)
            logger.info("Sauvegarde écrite dans le volume persistant.")
            return True
        except Exception as e:
            logger.error(f"Erreur de sauvegarde : {e}")
            return False
    return False


def load_saved_game():
    global player, current_user
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "player" in data:
                player = data["player"]
                current_user = data.get("user")
            elif isinstance(data, dict) and "class_id" in data:
                player = data

            if player:
                player.setdefault("dodge_chance", 0.20)
                player.setdefault("parry_reduction", 0.50)
                player.setdefault("parry_riposte", 0)
                player.setdefault("flee_chance", 0.45)
                player.setdefault("flee_safe", False)
                player.setdefault("pos_x", 0)
                player.setdefault("pos_y", 0)
                player.setdefault("visited_rooms", {"0,0": {"type": "start", "label": "Entrée"}})
                if "skill_tree" in player and player.get("class_id") in SKILL_TREES:
                    player["skill_tree"] = SKILL_TREES[player["class_id"]]
                return True
        except Exception as e:
            logger.error(f"Erreur chargement sauvegarde : {e}")
    return False


load_saved_game()


@app.after_request
def auto_save_after_action(response):
    if request.method in ["POST", "PUT"] and player:
        persist_save()
    return response


def check_level_up(p):
    leveled_up = False
    while p["xp"] >= p["xp_to_next"]:
        p["xp"] -= p["xp_to_next"]
        p["level"] += 1
        p["xp_to_next"] = int(p["xp_to_next"] * 1.5)
        p["skill_points"] += 1
        p["max_hp"] += 10
        p["hp"] = p["max_hp"]
        p["max_mp"] += 10
        p["mp"] = p["max_mp"]
        leveled_up = True
    return leveled_up


@app.route("/api", methods=["GET"])
def api():
    return jsonify({"status": "ok", "message": "Backend microservice opérationnel"})


@app.route("/api/register", methods=["POST"])
def register():
    global current_user
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"message": "Nom d'utilisateur et mot de passe requis !"}), 400

    if username in accounts:
        return jsonify({"message": "Ce nom d'utilisateur existe déjà !"}), 400

    accounts[username] = {
        "password": password,
        "high_score": 0,
        "level": 1,
        "class": "-"
    }
    save_accounts()
    current_user = username
    return jsonify({"message": f"Compte créé avec succès ! Bienvenue {username}.", "username": username})


@app.route("/api/login", methods=["POST"])
def login():
    global current_user
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if username not in accounts or accounts[username]["password"] != password:
        return jsonify({"message": "Identifiants incorrects !"}), 401

    current_user = username
    return jsonify({"message": f"Connexion réussie ! Content de te revoir, {username}.", "username": username})


@app.route("/api/leaderboard", methods=["GET"])
def leaderboard():
    sorted_players = []
    for user, info in accounts.items():
        sorted_players.append({
            "username": user,
            "high_score": info.get("high_score", 0),
            "level": info.get("level", 1),
            "class": info.get("class", "-")
        })
    sorted_players.sort(key=lambda x: x["high_score"], reverse=True)
    return jsonify({"leaderboard": sorted_players[:10]})


@app.route("/api/player_state", methods=["GET"])
def get_player_state():
    global player, current_user
    if not player:
        return jsonify({"error": "Aucun joueur actif.", "player": None, "user": current_user}), 404
    return jsonify({"player": player, "user": current_user})


@app.route("/api/select_class", methods=["POST"])
def select_class():
    global player, current_monster, current_event, current_merchant_stock

    data = request.get_json() or {}
    class_id = data.get("class_id", "empire")

    base_stats = CLASSES_STATS.get(class_id, CLASSES_STATS["empire"])
    skills_list = SKILL_TREES.get(class_id, [])

    player = {
        "class_id": class_id,
        "class_name": base_stats["name"],
        "level": 1,
        "xp": 0,
        "xp_to_next": 50,
        "gold": 30,
        "skill_points": 0,
        "unlocked_skills": [],
        "skill_tree": skills_list,
        "hp": base_stats["hp"],
        "max_hp": base_stats["hp"],
        "mp": 100,
        "max_mp": 100,
        "defense": base_stats["defense"],
        "dodge_chance": 0.20,
        "parry_reduction": 0.50,
        "parry_riposte": 0,
        "flee_chance": 0.45,
        "flee_safe": False,
        "weapon": dict(base_stats["weapon"]),
        "armor": {"name": "Tissu basique", "def": base_stats["defense"], "tier": 1, "desc": "Tenue de départ"},
        "inventory": [],
        "rooms_cleared": 0,
        "pos_x": 0,
        "pos_y": 0,
        "visited_rooms": {"0,0": {"type": "start", "label": "Entrée"}}
    }
    current_monster = None
    current_event = None
    current_merchant_stock = []

    persist_save()
    return jsonify({"message": f"Partie lancée en tant que {player['class_name']} !", "player": player})


@app.route("/api/save", methods=["POST"])
def save_endpoint():
    global player
    if not player:
        return jsonify({"message": "Aucune partie active à sauvegarder.", "player": None}), 400
    if persist_save():
        return jsonify({"message": "Partie sauvegardée dans le volume persistant Docker !", "player": player})
    return jsonify({"message": "Échec de l'écriture sur le volume.", "player": player}), 500


@app.route("/api/load", methods=["GET"])
def load_endpoint():
    global player, current_user
    if load_saved_game():
        return jsonify({"message": f"Partie restaurée ({player['class_name']} - Niv {player['level']}) !", "player": player, "user": current_user})
    return jsonify({"message": "Aucun fichier de sauvegarde trouvé dans le volume persistant.", "player": None}), 404


@app.route("/api/game_server_status", methods=["GET"])
def game_server_status():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((GAME_SERVER_HOST, GAME_SERVER_PORT))
        resp = s.recv(1024).decode('utf-8').strip()
        s.close()
        return jsonify({
            "status": "online",
            "network": "backend-net",
            "target": f"{GAME_SERVER_HOST}:{GAME_SERVER_PORT}",
            "response": resp
        })
    except Exception as e:
        return jsonify({
            "status": "offline",
            "network": "backend-net",
            "error": str(e)
        }), 503


@app.route("/api/draft_skills", methods=["GET"])
def draft_skills():
    global player
    if not player:
        return jsonify({"error": "Aucun joueur actif."}), 400

    available = [s for s in player["skill_tree"] if s["id"] not in player["unlocked_skills"]]
    choices = random.sample(available, min(3, len(available)))
    return jsonify({"choices": choices, "skill_points": player["skill_points"]})


@app.route("/api/learn_skill", methods=["POST"])
def learn_skill():
    global player
    if not player:
        return jsonify({"message": "Aucun joueur trouvé."}), 400

    data = request.get_json() or {}
    skill_id = data.get("skill_id")

    if player["skill_points"] <= 0:
        return jsonify({"message": "Aucun point de compétence disponible !"}), 400

    if skill_id in player["unlocked_skills"]:
        return jsonify({"message": "Compétence déjà débloquée !"}), 400

    target_skill = next((s for s in player["skill_tree"] if s["id"] == skill_id), None)
    if not target_skill:
        return jsonify({"message": "Compétence introuvable."}), 400

    player["skill_points"] -= 1
    player["unlocked_skills"].append(skill_id)

    stype = target_skill["type"]
    val = target_skill["val"]

    if stype == "hp_max":
        player["max_hp"] += val
        player["hp"] += val
    elif stype == "mp_max":
        player["max_mp"] += val
        player["mp"] += val
    elif stype == "def":
        player["defense"] += val
    elif stype == "dmg":
        player["weapon"]["min"] += val
        player["weapon"]["max"] += val
    elif stype == "dodge":
        player["dodge_chance"] = min(0.85, round(player.get("dodge_chance", 0.20) + val, 2))
    elif stype == "parry":
        player["parry_reduction"] = min(0.90, round(player.get("parry_reduction", 0.50) + 0.10, 2))
        player["parry_riposte"] = player.get("parry_riposte", 0) + val
    elif stype == "flee":
        player["flee_chance"] = min(0.95, round(player.get("flee_chance", 0.45) + val, 2))
        player["flee_safe"] = True

    return jsonify({"message": f"Compétence choisie : **{target_skill['name']}** !", "player": player})


@app.route("/api/move", methods=["POST"])
def move():
    global current_event, current_monster, current_merchant_stock, player

    if not player or player.get("hp", 0) <= 0:
        return jsonify({"error": "Aucun personnage sélectionné."}), 400

    data = request.get_json() or {}
    direction = data.get("direction", "Nord")

    if direction == "Nord":
        player["pos_y"] += 1
    elif direction == "Sud":
        player["pos_y"] -= 1
    elif direction == "Est":
        player["pos_x"] += 1
    elif direction == "Ouest":
        player["pos_x"] -= 1

    player["rooms_cleared"] += 1
    player["mp"] = min(player["max_mp"], player["mp"] + 10)
    pos_key = f"{player['pos_x']},{player['pos_y']}"

    if player["rooms_cleared"] % 5 == 0:
        current_event = "monster"
        b_template = random.choice(BOSSES_POOL)
        current_monster = {
            "name": b_template["name"],
            "hp": b_template["hp"],
            "max_hp": b_template["max_hp"],
            "atk_min": b_template["atk_min"],
            "atk_max": b_template["atk_max"],
            "xp": b_template["xp"],
            "gold_reward": b_template.get("gold_reward", 150),
            "is_boss": True
        }
        player["visited_rooms"][pos_key] = {"type": "boss", "label": "Boss"}
        msg = f"👑 **SALLE DU BOSS (Étage {player['rooms_cleared']}) !** Le **{current_monster['name']}** barre la route !"
        return jsonify({"event": "monster", "message": msg, "monster": current_monster, "player": player, "is_boss": True})

    rand = random.random()

    if rand < 0.20:
        current_event = "empty"
        current_monster = None
        player["visited_rooms"][pos_key] = {"type": "empty", "label": "Vide"}
        msg = f"Tu advances vers le {direction}... Les ruines sont calmes (+10 PM)."
        return jsonify({"event": "empty", "message": msg, "player": player})

    elif rand < 0.65:
        current_event = "monster"
        m_tier = min(5, ((player["rooms_cleared"] - 1) // 3) + 1)
        m_template = random.choice(MONSTERS_POOL[m_tier])
        current_monster = {
            "name": m_template["name"],
            "hp": m_template["hp"],
            "max_hp": m_template["max_hp"],
            "atk_min": m_template["atk_min"],
            "atk_max": m_template["atk_max"],
            "xp": m_template["xp"],
            "is_boss": False
        }
        player["visited_rooms"][pos_key] = {"type": "monster", "label": "Combat"}
        msg = f"Tu advances vers le {direction}... Un **{current_monster['name']}** surgit !"
        return jsonify({"event": "monster", "message": msg, "monster": current_monster, "player": player, "is_boss": False})

    elif rand < 0.80:
        current_event = "chest"
        current_monster = None
        tier = 1 if player["rooms_cleared"] <= 4 else (2 if player["rooms_cleared"] <= 8 else 3)
        class_weapons = [w for w in WEAPONS_BY_TIER[tier] if player["class_id"] in w["classes"]]
        class_armors = [a for a in ARMORS_BY_TIER[tier] if player["class_id"] in a["classes"]]

        selected_weapon = random.choice(class_weapons) if class_weapons else None
        selected_armor = random.choice(class_armors) if class_armors else None
        selected_item = random.choice(CONSUMABLES)
        chest_items = [item for item in [selected_weapon, selected_armor, selected_item] if item]
        random.shuffle(chest_items)

        player["visited_rooms"][pos_key] = {"type": "chest", "label": "Coffre"}
        msg = f"Tu advances vers le {direction}... Tu découvres un coffre béni !"
        return jsonify({"event": "chest", "message": msg, "chest": chest_items, "player": player})

    elif rand < 0.90:
        current_event = "merchant"
        current_monster = None
        tier = 1 if player["rooms_cleared"] <= 4 else (2 if player["rooms_cleared"] <= 8 else 3)
        class_weapons = [w for w in WEAPONS_BY_TIER[tier] if player["class_id"] in w["classes"]]
        class_armors = [a for a in ARMORS_BY_TIER[tier] if player["class_id"] in a["classes"]]

        w_item = dict(random.choice(class_weapons)) if class_weapons else dict(CONSUMABLES[0])
        a_item = dict(random.choice(class_armors)) if class_armors else dict(CONSUMABLES[1])
        c_item = dict(random.choice(CONSUMABLES))
        w_item["price"], a_item["price"], c_item["price"] = 35 * tier, 30 * tier, 15 * tier

        current_merchant_stock = [w_item, a_item, c_item]
        player["visited_rooms"][pos_key] = {"type": "merchant", "label": "Marchand"}
        msg = f"Tu advances vers le {direction}... Un marchand ambulant t'accueille !"
        return jsonify({"event": "merchant", "message": msg, "merchant_stock": current_merchant_stock, "player": player})

    else:
        current_monster = None
        if random.random() < 0.5:
            current_event = "altar"
            player["visited_rooms"][pos_key] = {"type": "altar", "label": "Autel"}
            msg = "⛩️ **Autel Ancien** : Souhaites-tu sacrifier 20 PV ?"
            return jsonify({"event": "altar", "message": msg, "player": player})
        else:
            current_event = "trap"
            trap_dmg = random.randint(8, 18)
            player["hp"] = max(1, player["hp"] - trap_dmg)
            player["visited_rooms"][pos_key] = {"type": "trap", "label": "Piège"}
            msg = f"⚠️ **PIÈGE !** Tu subis {trap_dmg} dégâts !"
            return jsonify({"event": "trap", "message": msg, "player": player})


@app.route("/api/interact_altar", methods=["POST"])
def interact_altar():
    global player, current_event
    if not player:
        return jsonify({"message": "Aucun joueur."}), 400

    data = request.get_json() or {}
    choice = data.get("choice")

    if choice == "sacrifice":
        if player["hp"] <= 20:
            msg = "Tu es trop faible pour accomplir ce rituel !"
        else:
            player["hp"] -= 20
            player["weapon"]["min"] += 3
            player["weapon"]["max"] += 5
            msg = "✨ **Pacte de Sang !** Tu sacrifies 20 PV mais ton arme gagne +3/+5 Dégâts permanents !"
    else:
        msg = "Tu te détournes de l'autel en toute sécurité."

    current_event = None
    return jsonify({"message": msg, "player": player})


@app.route("/api/buy_item", methods=["POST"])
def buy_item():
    global player, current_merchant_stock

    if not player:
        return jsonify({"message": "Aucun joueur."}), 400

    data = request.get_json() or {}
    item_index = data.get("index")

    if item_index is None or item_index >= len(current_merchant_stock):
        return jsonify({"message": "Article invalide."}), 400

    item = current_merchant_stock[item_index]
    price = item.get("price", 20)

    if player["gold"] < price:
        return jsonify({"message": f"Pas assez d'or ! Requis : {price} Gold.", "player": player, "merchant_stock": current_merchant_stock})

    player["gold"] -= price
    bought_item = current_merchant_stock.pop(item_index)

    if "min" in bought_item:
        player["weapon"] = bought_item
        msg = f"Tu achètes et équipes l'arme : **{bought_item['name']}** !"
    elif "def" in bought_item and "classes" in bought_item:
        old_armor_def = player["armor"].get("def", 0) if player.get("armor") else 0
        player["armor"] = bought_item
        player["defense"] = player["defense"] - old_armor_def + bought_item["def"]
        msg = f"Tu achètes et équipes l'armure : **{bought_item['name']}** !"
    else:
        if len(player["inventory"]) < 3:
            player["inventory"].append(bought_item)
            msg = f"Tu achètes **{bought_item['name']}** !"
        else:
            player["gold"] += price
            current_merchant_stock.insert(item_index, bought_item)
            msg = "Ton sac est plein ! Achat annulé."

    return jsonify({"message": msg, "player": player, "merchant_stock": current_merchant_stock})


@app.route("/api/attack", methods=["POST"])
def attack():
    global current_monster, player

    if not player or player.get("hp", 0) <= 0:
        return jsonify({"message": "Aucun héros actif."}), 400

    if not current_monster or current_monster.get("hp", 0) <= 0:
        return jsonify({"player": player, "monster": None, "message": "Aucun ennemi ici !", "player_dead": False, "monster_dead": True})

    p_damage = random.randint(player["weapon"]["min"], player["weapon"]["max"])
    current_monster["hp"] = max(0, current_monster["hp"] - p_damage)
    player["mp"] = min(player["max_mp"], player["mp"] + 5)

    log_msg = f"Tu attaques avec {player['weapon']['name']} (-{p_damage} HP, +5 PM)."

    if current_monster["hp"] > 0:
        raw_m_damage = random.randint(current_monster["atk_min"], current_monster["atk_max"])
        m_damage_dealt = max(1, raw_m_damage - player["defense"])
        player["hp"] = max(0, player["hp"] - m_damage_dealt)
        log_msg += f" Le {current_monster['name']} riposte ! (-{m_damage_dealt} HP)."
    else:
        xp_gained = current_monster["xp"]
        gold_gained = current_monster.get("gold_reward", random.randint(10, 25))
        player["xp"] += xp_gained
        player["gold"] += gold_gained
        log_msg += f" Le {current_monster['name']} s'effondre ! (+{xp_gained} XP, +{gold_gained} Gold)."
        if check_level_up(player):
            log_msg += f" **LEVEL UP !** Tu es maintenant Niveau {player['level']} ! (+1 Point de compétence)"

    return jsonify({
        "player": player,
        "monster": current_monster,
        "message": log_msg,
        "player_dead": player["hp"] <= 0,
        "monster_dead": current_monster["hp"] <= 0
    })


@app.route("/api/defend", methods=["POST"])
def defend():
    global current_monster, player

    if not player or player.get("hp", 0) <= 0:
        return jsonify({"message": "Aucun héros actif."}), 400

    if not current_monster or current_monster.get("hp", 0) <= 0:
        return jsonify({"player": player, "monster": None, "message": "Aucun ennemi ici !", "player_dead": False, "monster_dead": True})

    player["mp"] = min(player["max_mp"], player["mp"] + 15)
    is_dodge = random.random() < player.get("dodge_chance", 0.20)

    if is_dodge:
        log_msg = f"💨 **ESQUIVE PARFAITE !** Tu évites l'attaque du {current_monster['name']} (+15 PM) !"
    else:
        raw_m_damage = random.randint(current_monster["atk_min"], current_monster["atk_max"])
        base_dmg = max(1, raw_m_damage - player["defense"])
        red_factor = player.get("parry_reduction", 0.50)
        m_damage_dealt = max(1, int(base_dmg * (1.0 - red_factor)))
        player["hp"] = max(0, player["hp"] - m_damage_dealt)
        log_msg = f"🛡️ **POSTURE DÉFENSIVE !** Dégâts réduits de {int(red_factor*100)}% ! Le {current_monster['name']} inflige {m_damage_dealt} HP (+15 PM)."

    return jsonify({
        "player": player,
        "monster": current_monster,
        "message": log_msg,
        "player_dead": player["hp"] <= 0,
        "monster_dead": False
    })


@app.route("/api/special_attack", methods=["POST"])
def special_attack():
    global current_monster, player

    if not player or player.get("hp", 0) <= 0:
        return jsonify({"message": "Aucun héros actif."}), 400

    if not current_monster or current_monster.get("hp", 0) <= 0:
        return jsonify({"message": "Aucun ennemi à attaquer."})

    cost = 30
    if player["mp"] < cost:
        return jsonify({"message": "Pas assez de PM ! (Requis : 30 PM)", "player": player, "monster": current_monster})

    player["mp"] -= cost
    w_name = player["weapon"]["name"].lower()

    base_dmg = int(random.randint(player["weapon"]["min"], player["weapon"]["max"]) * 1.8)
    bonus_effect = ""

    if any(k in w_name for k in ["hache", "kikoup"]):
        base_dmg = int(base_dmg * 1.2)
        bonus_effect = "⚡ [Entaille Brutale] Dégâts massifs !"
    elif any(k in w_name for k in ["marteau", "masse", "fléau"]):
        bonus_effect = "🛡️ [Brise-Armure] Impact fracassant !"
    elif any(k in w_name for k in ["bâton", "sceptre", "orbe"]):
        heal_val = 15
        player["hp"] = min(player["max_hp"], player["hp"] + heal_val)
        bonus_effect = f"✨ [Explosion Arcanique] Magie & Soin (+{heal_val} PV) !"
    elif any(k in w_name for k in ["dague", "surin", "kris"]):
        player["defense"] += 1
        base_dmg = int(base_dmg * 1.3)
        bonus_effect = "🗡️ [Coup Furtif] Critique & +1 Défense !"
    elif any(k in w_name for k in ["arc", "arbalète"]):
        bonus_effect = "🏹 [Tir Perforant] Flèche dévastatrice !"
    else:
        base_dmg = int(base_dmg * 1.4)
        bonus_effect = "⚔️ [Frappe Héroïque] Coup surpuissant !"

    current_monster["hp"] = max(0, current_monster["hp"] - base_dmg)
    log_msg = f"✨ **COUP SPÉCIAL !** {bonus_effect} (-{base_dmg} HP)."

    if current_monster["hp"] > 0:
        raw_m_damage = random.randint(current_monster["atk_min"], current_monster["atk_max"])
        m_damage_dealt = max(1, raw_m_damage - player["defense"])
        player["hp"] = max(0, player["hp"] - m_damage_dealt)
        log_msg += f" Le {current_monster['name']} riposte ! (-{m_damage_dealt} HP)."
    else:
        xp_gained = current_monster["xp"]
        gold_gained = current_monster.get("gold_reward", random.randint(10, 25))
        player["xp"] += xp_gained
        player["gold"] += gold_gained
        log_msg += f" Le {current_monster['name']} est anéanti ! (+{xp_gained} XP, +{gold_gained} Gold)."
        if check_level_up(player):
            log_msg += f" **LEVEL UP !** Tu es maintenant Niveau {player['level']} ! (+1 Point de compétence)"

    return jsonify({
        "player": player,
        "monster": current_monster,
        "message": log_msg,
        "player_dead": player["hp"] <= 0,
        "monster_dead": current_monster["hp"] <= 0
    })


@app.route("/api/flee", methods=["POST"])
def flee():
    global current_monster, current_event, player

    if not player or player.get("hp", 0) <= 0:
        return jsonify({"message": "Aucun héros actif."}), 400

    if not current_monster or current_monster.get("hp", 0) <= 0:
        return jsonify({"player": player, "monster": None, "message": "Aucun ennemi à fuir !", "fled": True})

    if current_monster.get("is_boss"):
        return jsonify({
            "player": player,
            "monster": current_monster,
            "message": "🚫 **IMPOSSIBLE DE FUIR !** La présence terrifiante du Boss bloque toute sortie !",
            "fled": False,
            "player_dead": False
        })

    f_chance = player.get("flee_chance", 0.45)
    success = random.random() < f_chance

    if success:
        gold_lost = int(player["gold"] * random.uniform(0.2, 0.4)) if not player.get("flee_safe") else 0
        player["gold"] = max(0, player["gold"] - gold_lost)
        flee_damage = random.randint(5, 12) if not player.get("flee_safe") else 0
        player["hp"] = max(1, player["hp"] - flee_damage)

        current_monster = None
        current_event = None

        log_msg = f"💨 **FUITE DÉSESPÉRÉE !** Tu t'enfuis en panique (-{flee_damage} PV). "
        if gold_lost > 0:
            log_msg += f"Dans la précipitation, tu fais tomber **{gold_lost} Or** !"

        return jsonify({
            "player": player,
            "monster": None,
            "message": log_msg,
            "fled": True,
            "player_dead": False
        })
    else:
        raw_m_damage = random.randint(current_monster["atk_min"], current_monster["atk_max"])
        m_damage_dealt = max(1, int((raw_m_damage - player["defense"]) * 1.5))
        player["hp"] = max(0, player["hp"] - m_damage_dealt)
        player["mp"] = max(0, player["mp"] - 15)

        log_msg = f"💀 **ÉCHEC DE LA FUITE !** Le {current_monster['name']} te frappe mortellement dans le dos ! (**-{m_damage_dealt} PV**, **-15 PM**)."

        return jsonify({
            "player": player,
            "monster": current_monster,
            "message": log_msg,
            "fled": False,
            "player_dead": player["hp"] <= 0
        })


@app.route("/api/equip", methods=["POST"])
def equip():
    global player

    if not player:
        return jsonify({"message": "Aucun joueur.", "player": None}), 400

    data = request.get_json() or {}
    chosen_item = data.get("item")

    if chosen_item:
        if "min" in chosen_item:
            player["weapon"] = chosen_item
            msg = f"Tu équipes l'arme : {player['weapon']['name']} !"
        elif "def" in chosen_item and "classes" in chosen_item:
            old_armor_def = player["armor"].get("def", 0) if player.get("armor") else 0
            player["armor"] = chosen_item
            player["defense"] = player["defense"] - old_armor_def + chosen_item["def"]
            msg = f"Tu équipes l'armure : {player['armor']['name']} (+{chosen_item['def']} Def) !"
        else:
            if len(player["inventory"]) < 3:
                player["inventory"].append(chosen_item)
                msg = f"Tu ajoutes {chosen_item['name']} dans ton sac !"
            else:
                msg = "Sac plein ! Impossible de prendre cet objet."
    else:
        msg = "Tu laisses le coffre intact."

    return jsonify({"message": msg, "player": player})


@app.route("/api/use_item", methods=["POST"])
def use_item():
    global player, current_monster, current_event

    if not player:
        return jsonify({"message": "Aucun joueur."}), 400

    data = request.get_json() or {}
    item_index = data.get("index")

    if item_index is None or item_index >= len(player["inventory"]):
        return jsonify({"message": "Objet invalide."}), 400

    item = player["inventory"].pop(item_index)
    msg = f"Tu utilises {item['name']} ! "

    if item["type"] == "heal":
        player["hp"] = min(player["max_hp"], player["hp"] + item["value"])
    elif item["type"] == "def_buff":
        player["defense"] += item["value"]
    elif item["type"] == "hp_max_buff":
        player["max_hp"] += item["value"]
        player["hp"] += item["value"]
    elif item["type"] == "damage" and current_monster:
        current_monster["hp"] = max(0, current_monster["hp"] - item["value"])
        if current_monster["hp"] == 0:
            msg += " Le monstre est anéanti !"
    elif item["type"] == "teleport" and current_monster:
        current_monster = None
        current_event = None
        msg += " Tu te téléportes en sécurité hors de la salle !"

    return jsonify({"message": msg, "player": player, "monster": current_monster})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
