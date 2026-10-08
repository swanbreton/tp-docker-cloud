import signal
import sys
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from game_data import CLASSES_STATS, SKILL_TREES, WEAPONS_BY_TIER, ARMORS_BY_TIER, MONSTERS_POOL, CONSUMABLES

app = Flask(__name__)
CORS(app)

signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))

player = None
current_event = None
current_monster = None
current_merchant_stock = []

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
    return jsonify({"status": "ok"})

@app.route("/api/player_state", methods=["GET"])
def get_player_state():
    global player
    if not player:
        return jsonify({"error": "Aucun joueur actif.", "player": None}), 404
    return jsonify({"player": player})

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
        "weapon": dict(base_stats["weapon"]),
        "armor": {"name": "Tissu basique", "def": base_stats["defense"], "tier": 1, "desc": "Tenue de départ"},
        "inventory": [],
        "rooms_cleared": 0
    }
    current_monster = None
    current_event = None
    current_merchant_stock = []

    return jsonify({"message": f"Partie lancée en tant que {player['class_name']} !", "player": player})

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

    return jsonify({"message": f"Compétence choisie : **{target_skill['name']}** !", "player": player})

@app.route("/api/move", methods=["POST"])
def move():
    global current_event, current_monster, current_merchant_stock, player

    if not player or player.get("hp", 0) <= 0:
        return jsonify({"error": "Aucun personnage sélectionné."}), 400

    data = request.get_json() or {}
    direction = data.get("direction", "Nord")
    player["rooms_cleared"] += 1

    player["mp"] = min(player["max_mp"], player["mp"] + 10)

    rand = random.random()
    
    # 20% Salle vide
    if rand < 0.20:
        current_event = "empty"
        current_monster = None
        msg = f"Tu advances vers le {direction}... Les ruines sombres sont calmes (+10 PM)."
        return jsonify({"event": "empty", "message": msg, "player": player})

    # 45% Combat contre un monstre
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
            "xp": m_template["xp"]
        }
        msg = f"Tu advances vers le {direction}... Un **{current_monster['name']}** surgit du Chaos !"
        return jsonify({"event": "monster", "message": msg, "monster": current_monster, "player": player})

    # 15% Coffre
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

        msg = f"Tu advances vers le {direction}... Tu découvres un coffre béni !"
        return jsonify({"event": "chest", "message": msg, "chest": chest_items, "player": player})

    # 10% Marchand PNJ
    elif rand < 0.90:
        current_event = "merchant"
        current_monster = None
        tier = 1 if player["rooms_cleared"] <= 4 else (2 if player["rooms_cleared"] <= 8 else 3)

        class_weapons = [w for w in WEAPONS_BY_TIER[tier] if player["class_id"] in w["classes"]]
        class_armors = [a for a in ARMORS_BY_TIER[tier] if player["class_id"] in a["classes"]]

        w_item = dict(random.choice(class_weapons)) if class_weapons else dict(CONSUMABLES[0])
        a_item = dict(random.choice(class_armors)) if class_armors else dict(CONSUMABLES[1])
        c_item = dict(random.choice(CONSUMABLES))

        w_item["price"] = 35 * tier
        a_item["price"] = 30 * tier
        c_item["price"] = 15 * tier

        current_merchant_stock = [w_item, a_item, c_item]
        msg = f"Tu advances vers le {direction}... Un marchand ambulant t'accueille dans l'ombre !"
        return jsonify({"event": "merchant", "message": msg, "merchant_stock": current_merchant_stock, "player": player})

    # 10% Événement / Piège / Autel
    else:
        current_monster = None
        sub_rand = random.random()

        if sub_rand < 0.5:
            current_event = "altar"
            msg = "⛩️ **Autel Ancien** : Un autel baigne dans une lueur mystique. Souhaites-tu sacrifier 20 PV contre de la puissance ?"
            return jsonify({"event": "altar", "message": msg, "player": player})
        else:
            current_event = "trap"
            trap_dmg = random.randint(8, 18)
            player["hp"] = max(1, player["hp"] - trap_dmg)
            msg = f"⚠️ **PIÈGE !** Des piques jaillissent des murs ! Tu subis {trap_dmg} dégâts !"
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
        gold_gained = random.randint(10, 25)
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
    is_dodge = random.random() < 0.20

    if is_dodge:
        log_msg = f"💨 **ESQUIVE PARFAITE !** Tu évites l'attaque du {current_monster['name']} (+15 PM) !"
    else:
        raw_m_damage = random.randint(current_monster["atk_min"], current_monster["atk_max"])
        base_dmg = max(1, raw_m_damage - player["defense"])
        m_damage_dealt = max(1, int(base_dmg * 0.5))
        player["hp"] = max(0, player["hp"] - m_damage_dealt)
        log_msg = f"🛡️ **POSTURE DÉFENSIVE !** Dégâts réduits de 50% ! Le {current_monster['name']} inflige {m_damage_dealt} HP (+15 PM)."

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
        gold_gained = random.randint(10, 25)
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

    # Fuite punitive : 45% de chances de réussite
    success = random.random() < 0.45

    if success:
        gold_lost = int(player["gold"] * random.uniform(0.2, 0.4))
        player["gold"] = max(0, player["gold"] - gold_lost)
        
        flee_damage = random.randint(5, 12)
        player["hp"] = max(1, player["hp"] - flee_damage)
        
        current_monster = None
        current_event = None
        
        log_msg = f"💨 **FUITE DÉSESPÉRÉE !** Tu t'enfuis en panique (-{flee_damage} PV). Dans la précipitation, tu fais tomber **{gold_lost} Or** !"
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
    app.run(host="0.0.0.0", port=5000)