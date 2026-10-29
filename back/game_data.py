CLASSES_STATS = {
    "empire": {
        "name": "Garde Franc de l'Empire",
        "hp": 110, "max_hp": 110, "defense": 3,
        "weapon": {"name": "Épée longue d'Altdorf", "min": 8, "max": 16, "tier": 1, "desc": "Équilibrée"}
    },
    "slayer": {
        "name": "Tueur Nain (Slayer)",
        "hp": 90, "max_hp": 90, "defense": 0,
        "weapon": {"name": "Double Hache du Tueur", "min": 14, "max": 24, "tier": 1, "desc": "Très offensif"}
    },
    "sigmar": {
        "name": "Prêtre-Guerrier de Sigmar",
        "hp": 130, "max_hp": 130, "defense": 5,
        "weapon": {"name": "Marteau des Pénitents", "min": 6, "max": 14, "tier": 1, "desc": "Résistant"}
    },
    "elfe": {
        "name": "Maître-Aigle Haut-Elfe",
        "hp": 85, "max_hp": 85, "defense": 1,
        "weapon": {"name": "Arc d'Avelorn", "min": 10, "max": 22, "tier": 1, "desc": "Tir de précision"}
    },
    "bright_wizard": {
        "name": "Sorcier Flamboyant",
        "hp": 80, "max_hp": 80, "defense": 0,
        "weapon": {"name": "Bâton d'Ambre", "min": 5, "max": 28, "tier": 1, "desc": "Magie instable"}
    },
    "khainite": {
        "name": "Assassin Khainite",
        "hp": 95, "max_hp": 95, "defense": 2,
        "weapon": {"name": "Dagues de l'Ombre", "min": 11, "max": 19, "tier": 1, "desc": "Attaques critiques"}
    }
}

SKILL_TREES = {
    "empire": [
        {"id": "emp_1", "name": "Discipline d'Altdorf", "desc": "+15 PV Max", "type": "hp_max", "val": 15},
        {"id": "emp_2", "name": "Armure de Plaque", "desc": "+3 Défense", "type": "def", "val": 3},
        {"id": "emp_3", "name": "Fente du Reikland", "desc": "+5 Dégâts Min/Max", "type": "dmg", "val": 5},
        {"id": "emp_4", "name": "Parade au Pavois", "desc": "+20% Parade & Riposte de 10 Dégâts", "type": "parry", "val": 10},
        {"id": "emp_5", "name": "Repli Tactique Ordonné", "desc": "+25% Chance de Fuite & 0 Dégât", "type": "flee", "val": 0.25},
        {"id": "emp_6", "name": "Maîtrise d'Escrime", "desc": "+7 Dégâts Min/Max", "type": "dmg", "val": 7},
        {"id": "emp_7", "name": "Pas de Côté Discipliné", "desc": "+15% Chance d'Esquive totale", "type": "dodge", "val": 0.15},
        {"id": "emp_8", "name": "Détermination du Reik", "desc": "+30 PM Max", "type": "mp_max", "val": 30},
        {"id": "emp_9", "name": "Garde Inébranlable", "desc": "+25% Parade & Riposte de 15 Dégâts", "type": "parry", "val": 15},
        {"id": "emp_10", "name": "Frappe du Maréchal", "desc": "+12 Dégâts Min/Max", "type": "dmg", "val": 12},
        {"id": "emp_11", "name": "Esquive Vétéran", "desc": "+20% Chance d'Esquive totale", "type": "dodge", "val": 0.20},
        {"id": "emp_12", "name": "Désengagement Stratégique", "desc": "+30% Chance de Fuite & 0 Or perdu", "type": "flee", "val": 0.30}
    ],
    "slayer": [
        {"id": "sla_1", "name": "Serment du Tueur", "desc": "+8 Dégâts Min/Max", "type": "dmg", "val": 8},
        {"id": "sla_2", "name": "Fureur Incorruptible", "desc": "+25 PV Max", "type": "hp_max", "val": 25},
        {"id": "sla_3", "name": "Parade Hache-Croisée", "desc": "+20% Parade & Riposte de 14 Dégâts", "type": "parry", "val": 14},
        {"id": "sla_4", "name": "Rage Berserker", "desc": "+10 Dégâts Min/Max", "type": "dmg", "val": 10},
        {"id": "sla_5", "name": "Endurance des Montagnes", "desc": "+30 PV Max", "type": "hp_max", "val": 30},
        {"id": "sla_6", "name": "Esquive Réflexe du Tueur", "desc": "+15% Chance d'Esquive réflexe", "type": "dodge", "val": 0.15},
        {"id": "sla_7", "name": "Haches Sanglantes", "desc": "+12 Dégâts Min/Max", "type": "dmg", "val": 12},
        {"id": "sla_8", "name": "Ruée de Dégagement", "desc": "+25% Chance de Fuite sans dégâts", "type": "flee", "val": 0.25},
        {"id": "sla_9", "name": "Riposte Féroce de Gromril", "desc": "+25% Parade & Riposte de 18 Dégâts", "type": "parry", "val": 18},
        {"id": "sla_10", "name": "Tueur de Démons", "desc": "+15 Dégâts Min/Max", "type": "dmg", "val": 15},
        {"id": "sla_11", "name": "Esquive Sauvage", "desc": "+20% Chance d'Esquive totale", "type": "dodge", "val": 0.20},
        {"id": "sla_12", "name": "Désengagement Berserk", "desc": "+30% Chance de Fuite héroïque", "type": "flee", "val": 0.30}
    ],
    "sigmar": [
        {"id": "sig_1", "name": "Foi Inébranlable", "desc": "+4 Défense", "type": "def", "val": 4},
        {"id": "sig_2", "name": "Bénédiction Divine", "desc": "+30 PV Max", "type": "hp_max", "val": 30},
        {"id": "sig_3", "name": "Égide Sacrée de Sigmar", "desc": "+25% Parade & Châtiment de 12 Dégâts", "type": "parry", "val": 12},
        {"id": "sig_4", "name": "Zèle du Fanatique", "desc": "+35 PM Max", "type": "mp_max", "val": 35},
        {"id": "sig_5", "name": "Pas Saint & Grâce Divine", "desc": "+15% Chance d'Esquive bénie", "type": "dodge", "val": 0.15},
        {"id": "sig_6", "name": "Ferveur Sacrée", "desc": "+6 Dégâts Min/Max", "type": "dmg", "val": 6},
        {"id": "sig_7", "name": "Retraite Pénitente", "desc": "+30% Chance de Fuite & 0 Or perdu", "type": "flee", "val": 0.30},
        {"id": "sig_8", "name": "Comète à Deux Queues", "desc": "+40 PM Max", "type": "mp_max", "val": 40},
        {"id": "sig_9", "name": "Parade Sanctifiée", "desc": "+30% Parade & Riposte de 16 Dégâts", "type": "parry", "val": 16},
        {"id": "sig_10", "name": "Justice Divine", "desc": "+10 Dégâts Min/Max", "type": "dmg", "val": 10},
        {"id": "sig_11", "name": "Esquive de Lumière", "desc": "+20% Chance d'Esquive sacrée", "type": "dodge", "val": 0.20},
        {"id": "sig_12", "name": "Sanctuaire de Retraite", "desc": "+35% Chance de Fuite miraculeuse", "type": "flee", "val": 0.35}
    ],
    "elfe": [
        {"id": "elf_1", "name": "Œil d'Avelorn", "desc": "+6 Dégâts Min/Max", "type": "dmg", "val": 6},
        {"id": "elf_2", "name": "Grâce d'Ulthuan", "desc": "+30 PM Max", "type": "mp_max", "val": 30},
        {"id": "elf_3", "name": "Danse des Brumes Aériennes", "desc": "+25% Chance d'Esquive acrobatique", "type": "dodge", "val": 0.25},
        {"id": "elf_4", "name": "Parade du Maître des Épées", "desc": "+20% Parade & Riposte de 12 Dégâts", "type": "parry", "val": 12},
        {"id": "elf_5", "name": "Focus Arcanique", "desc": "+40 PM Max", "type": "mp_max", "val": 40},
        {"id": "elf_6", "name": "Évanescence d'Ulthuan", "desc": "+35% Chance de Fuite sans perte d'or", "type": "flee", "val": 0.35},
        {"id": "elf_7", "name": "Flèches Stellaires", "desc": "+10 Dégâts Min/Max", "type": "dmg", "val": 10},
        {"id": "elf_8", "name": "Esquive Suprême d'Isha", "desc": "+25% Chance d'Esquive parfaite", "type": "dodge", "val": 0.25},
        {"id": "elf_9", "name": "Riposte Stellaire", "desc": "+25% Parade & Riposte de 15 Dégâts", "type": "parry", "val": 15},
        {"id": "elf_10", "name": "Maître-Archer", "desc": "+14 Dégâts Min/Max", "type": "dmg", "val": 14},
        {"id": "elf_11", "name": "Passe d'Invisibilité", "desc": "+40% Chance de Fuite sans trace", "type": "flee", "val": 0.40},
        {"id": "elf_12", "name": "Reflet d'Argent", "desc": "+25 PV Max", "type": "hp_max", "val": 25}
    ],
    "bright_wizard": [
        {"id": "wiz_1", "name": "Vents d'Aqshy", "desc": "+50 PM Max", "type": "mp_max", "val": 50},
        {"id": "wiz_2", "name": "Incinération Suprême", "desc": "+7 Dégâts Min/Max", "type": "dmg", "val": 7},
        {"id": "wiz_3", "name": "Illusion de Cendres", "desc": "+20% Chance d'Esquive vaporeuse", "type": "dodge", "val": 0.20},
        {"id": "wiz_4", "name": "Barrière Incandescente", "desc": "+20% Parade & Brûlure de riposte de 14 Dégâts", "type": "parry", "val": 14},
        {"id": "wiz_5", "name": "Bouclier de Magma", "desc": "+3 Défense", "type": "def", "val": 3},
        {"id": "wiz_6", "name": "Téléportation Flamboyante", "desc": "+35% Chance de Fuite en nuage de feu", "type": "flee", "val": 0.35},
        {"id": "wiz_7", "name": "Cœur de Braise", "desc": "+30 PV Max", "type": "hp_max", "val": 30},
        {"id": "wiz_8", "name": "Esquive de Flamme Vive", "desc": "+25% Chance d'Esquive incandescente", "type": "dodge", "val": 0.25},
        {"id": "wiz_9", "name": "Parade Explosive d'Aqshy", "desc": "+25% Parade & Déflagration de riposte de 18 Dégâts", "type": "parry", "val": 18},
        {"id": "wiz_10", "name": "Cataclysme d'Aqshy", "desc": "+16 Dégâts Min/Max", "type": "dmg", "val": 16},
        {"id": "wiz_11", "name": "Fuite en Traînée de Feu", "desc": "+40% Chance de Fuite magique sans perte", "type": "flee", "val": 0.40},
        {"id": "wiz_12", "name": "Pacte du Phénix", "desc": "+60 PM Max", "type": "mp_max", "val": 60}
    ],
    "khainite": [
        {"id": "kha_1", "name": "Lame Empoisonnée", "desc": "+7 Dégâts Min/Max", "type": "dmg", "val": 7},
        {"id": "kha_2", "name": "Esquive Fantomatique de Khaine", "desc": "+25% Chance d'Esquive des ombres", "type": "dodge", "val": 0.25},
        {"id": "kha_3", "name": "Parade Empoisonnée & Riposte", "desc": "+25% Parade & Riposte toxique de 16 Dégâts", "type": "parry", "val": 16},
        {"id": "kha_4", "name": "Disparition dans les Ombres", "desc": "+40% Chance de Fuite furtive garantie", "type": "flee", "val": 0.40},
        {"id": "kha_5", "name": "Poisons Subtils", "desc": "+8 Dégâts Min/Max", "type": "dmg", "val": 8},
        {"id": "kha_6", "name": "Pas de l'Ombre Insaisissable", "desc": "+20% Chance d'Esquive mortelle", "type": "dodge", "val": 0.20},
        {"id": "kha_7", "name": "Frappe Anonyme", "desc": "+11 Dégâts Min/Max", "type": "dmg", "val": 11},
        {"id": "kha_8", "name": "Riposte Foudroyante de Khaine", "desc": "+25% Parade & Assassinat de riposte de 20 Dégâts", "type": "parry", "val": 20},
        {"id": "kha_9", "name": "Échappatoire de la Mante", "desc": "+35% Chance de Fuite sans bruit, 0 or et 0 PV", "type": "flee", "val": 0.35},
        {"id": "kha_10", "name": "Danse de la Mort", "desc": "+15 Dégâts Min/Max", "type": "dmg", "val": 15},
        {"id": "kha_11", "name": "Esquive Réflexe de l'Assassin", "desc": "+15% Chance d'Esquive réflexe", "type": "dodge", "val": 0.15},
        {"id": "kha_12", "name": "Vampirisme de Khaine", "desc": "+25 PV Max", "type": "hp_max", "val": 25}
    ]
}

CONSUMABLES = [
    {"id": "potion_shallya", "name": "Potion de Shallya", "type": "heal", "value": 40, "desc": "Soigne 40 PV"},
    {"id": "elixir_vitalite", "name": "Élixir de Vitalité Elfe", "type": "heal", "value": 75, "desc": "Soigne 75 PV"},
    {"id": "elixir_sigmar", "name": "Élixir de Sigmar", "type": "def_buff", "value": 2, "desc": "+2 Défense permanente"},
    {"id": "peau_ecorce", "name": "Bénédiction de Ghyran", "type": "def_buff", "value": 4, "desc": "+4 Défense permanente"},
    {"id": "potion_fureur", "name": "Brew du Tueur Nain", "type": "hp_max_buff", "value": 20, "desc": "+20 PV Max & soigne 20 PV"},
    {"id": "bombe_malepierre", "name": "Bombe de Malepierre", "type": "damage", "value": 50, "desc": "Inflige 50 dégâts instantanés"},
    {"id": "grenade_feu_enfer", "name": "Grenade d'Altdorf", "type": "damage", "value": 90, "desc": "Inflige 90 dégâts de feu instantanés"},
    {"id": "fiole_venin", "name": "Venin de Serpents d'Ulgu", "type": "damage", "value": 130, "desc": "Inflige 130 dégâts toxiques"},
    {"id": "parchemin_azyr", "name": "Parchemin d'Azyr", "type": "teleport", "value": 0, "desc": "Esquive le combat et valide la salle"},
    {"id": "orbe_ombre", "name": "Orbe d'Ombre d'Ulgu", "type": "teleport", "value": 0, "desc": "Fuite instantanée sans subir de riposte"}
]

WEAPONS_BY_TIER = {
    1: [
        {"name": "Épée courte de l'Empire", "min": 8, "max": 14, "tier": 1, "desc": "Standard d'Altdorf", "classes": ["empire"]},
        {"name": "Hallebarde de Milicien", "min": 9, "max": 17, "tier": 1, "desc": "Allonge efficace", "classes": ["empire"]},
        {"name": "Rapière d'Estalie", "min": 7, "max": 15, "tier": 1, "desc": "Précision d'estoc", "classes": ["empire"]},
        {"name": "Hachette en fer Nain", "min": 10, "max": 18, "tier": 1, "desc": "Tranchant brut", "classes": ["slayer"]},
        {"name": "Double Hache d'entraînement", "min": 12, "max": 20, "tier": 1, "desc": "Style berserker", "classes": ["slayer"]},
        {"name": "Hache de jet lourde", "min": 11, "max": 19, "tier": 1, "desc": "Impact direct", "classes": ["slayer"]},
        {"name": "Masse cloutée de Pénitent", "min": 7, "max": 15, "tier": 1, "desc": "Contondant", "classes": ["sigmar"]},
        {"name": "Marteau de bois béni", "min": 6, "max": 14, "tier": 1, "desc": "Foi de Sigmar", "classes": ["sigmar"]},
        {"name": "Sceptre de foi de Nuln", "min": 8, "max": 13, "tier": 1, "desc": "Prière protectrice", "classes": ["sigmar"]},
        {"name": "Arc court de Chasseur", "min": 8, "max": 18, "tier": 1, "desc": "Tir rapide", "classes": ["elfe"]},
        {"name": "Lame fine d'Ulthuan", "min": 9, "max": 16, "tier": 1, "desc": "Gracieuse", "classes": ["elfe"]},
        {"name": "Arc d'Infanterie Elfe", "min": 10, "max": 20, "tier": 1, "desc": "Portée moyenne", "classes": ["elfe"]},
        {"name": "Bâton d'apprenti d'Ambre", "min": 5, "max": 22, "tier": 1, "desc": "Étincelles magiques", "classes": ["bright_wizard"]},
        {"name": "Sceptre d'Incinération", "min": 4, "max": 25, "tier": 1, "desc": "Flammes mineures", "classes": ["bright_wizard"]},
        {"name": "Bâton de cendre", "min": 6, "max": 20, "tier": 1, "desc": "Chaleur arcanique", "classes": ["bright_wizard"]},
        {"name": "Surin d'Assassin", "min": 10, "max": 16, "tier": 1, "desc": "Lame empoisonnée", "classes": ["khainite"]},
        {"name": "Dague de jet Khainite", "min": 9, "max": 18, "tier": 1, "desc": "Furtive", "classes": ["khainite"]},
        {"name": "Kris en ébonite", "min": 11, "max": 17, "tier": 1, "desc": "Perce-armure", "classes": ["khainite"]}
    ],
    2: [
        {"name": "Épée à deux mains de Joueur d'Épée", "min": 18, "max": 28, "tier": 2, "desc": "Garde d'élite", "classes": ["empire"]},
        {"name": "Hallebarde de Reikland", "min": 20, "max": 30, "tier": 2, "desc": "Arme de haste puissante", "classes": ["empire"]},
        {"name": "Pistolet à répétition de Nuln", "min": 16, "max": 34, "tier": 2, "desc": "Poudre noire", "classes": ["empire"]},
        {"name": "Grande Hache du Tueur de Dragons", "min": 22, "max": 34, "tier": 2, "desc": "Dégâts brutaux", "classes": ["slayer"]},
        {"name": "Haches jumelles runiques", "min": 24, "max": 32, "tier": 2, "desc": "Inscrites de runes", "classes": ["slayer"]},
        {"name": "Hache d'Arme de Karak Kadrin", "min": 21, "max": 35, "tier": 2, "desc": "Forcée dans la roche", "classes": ["slayer"]},
        {"name": "Marteau de Guerre Sacré", "min": 18, "max": 26, "tier": 2, "desc": "Bénédiction du Marteau", "classes": ["sigmar"]},
        {"name": "Grand Marteau de Comète", "min": 20, "max": 28, "tier": 2, "desc": "Coup de grâce", "classes": ["sigmar"]},
        {"name": "Fléau des Flagellants", "min": 17, "max": 31, "tier": 2, "desc": "Fureur fanatique", "classes": ["sigmar"]},
        {"name": "Arc long d'Avelorn", "min": 16, "max": 36, "tier": 2, "desc": "Flèches de lumière", "classes": ["elfe"]},
        {"name": "Lame des Gardes Phénix", "min": 18, "max": 32, "tier": 2, "desc": "Flammes sacrées", "classes": ["elfe"]},
        {"name": "Arc de patrouilleur de Nagarythe", "min": 15, "max": 38, "tier": 2, "desc": "Tir mortel", "classes": ["elfe"]},
        {"name": "Bâton de Volcanisme", "min": 12, "max": 42, "tier": 2, "desc": "Éruption arcanique", "classes": ["bright_wizard"]},
        {"name": "Orbe de Pyromaître", "min": 10, "max": 45, "tier": 2, "desc": "Explosions de feu", "classes": ["bright_wizard"]},
        {"name": "Sceptre des Flammes d'Aqshy", "min": 14, "max": 40, "tier": 2, "desc": "Surchauffe pure", "classes": ["bright_wizard"]},
        {"name": "Dagues d'Ombre d'Ulgu", "min": 16, "max": 34, "tier": 2, "desc": "Siphon de sang", "classes": ["khainite"]},
        {"name": "Arbalète à répétition sombre", "min": 22, "max": 30, "tier": 2, "desc": "Rafale de carreaux", "classes": ["khainite"]},
        {"name": "Lame de supplice de Har Ganeth", "min": 18, "max": 33, "tier": 2, "desc": "Entaille toxique", "classes": ["khainite"]}
    ],
    3: [
        {"name": "Croc de Runes d'Altdorf", "min": 36, "max": 54, "tier": 3, "desc": "Lame d'Électeur", "classes": ["empire"]},
        {"name": "Lance du Maréchal de l'Empire", "min": 40, "max": 58, "tier": 3, "desc": "Charge glorieuse", "classes": ["empire"]},
        {"name": "Marteau d'Orichalque de Karl Franz", "min": 38, "max": 62, "tier": 3, "desc": "Puissance suprême", "classes": ["empire"]},
        {"name": "Hache du Tueur de Démons", "min": 38, "max": 68, "tier": 3, "desc": "Rune majeure de Mort", "classes": ["slayer"]},
        {"name": "Haches Légendaires de Grimnir", "min": 42, "max": 72, "tier": 3, "desc": "Fureur divine", "classes": ["slayer"]},
        {"name": "Fend-Roc du Haut Roi Nain", "min": 40, "max": 70, "tier": 3, "desc": "Détruit les armures", "classes": ["slayer"]},
        {"name": "Ghal Maraz (Copie Bénie)", "min": 40, "max": 52, "tier": 3, "desc": "Marteau céleste de Sigmar", "classes": ["sigmar"]},
        {"name": "Sceptre du Grand Théogoniste", "min": 36, "max": 58, "tier": 3, "desc": "Bénédiction divine", "classes": ["sigmar"]},
        {"name": "Marteau de Châtiment d'Azyr", "min": 42, "max": 60, "tier": 3, "desc": "Foudre céleste", "classes": ["sigmar"]},
        {"name": "Arc d'Astarielle", "min": 28, "max": 80, "tier": 3, "desc": "Traits solaires", "classes": ["elfe"]},
        {"name": "Lame Stellaire d'Ulthuan", "min": 38, "max": 62, "tier": 3, "desc": "Acier stellaire", "classes": ["elfe"]},
        {"name": "Grand Arc du Dragon d'Avelorn", "min": 32, "max": 76, "tier": 3, "desc": "Tir perforant sacré", "classes": ["elfe"]},
        {"name": "Bâton du Cataclysme d'Aqshy", "min": 20, "max": 100, "tier": 3, "desc": "Brasier infernal", "classes": ["bright_wizard"]},
        {"name": "Orbe du Phénix Flamboyant", "min": 25, "max": 90, "tier": 3, "desc": "Explosion d'énergie", "classes": ["bright_wizard"]},
        {"name": "Sceptre de Tempête de Feu", "min": 30, "max": 85, "tier": 3, "desc": "Feu dévastateur", "classes": ["bright_wizard"]},
        {"name": "Lame des Mille Entailles de Khaine", "min": 34, "max": 66, "tier": 3, "desc": "Soif de sang Khainite", "classes": ["khainite"]},
        {"name": "Dague de Mort de Hellebron", "min": 30, "max": 74, "tier": 3, "desc": "Exécution instantanée", "classes": ["khainite"]},
        {"name": "Épée d'Ébonite d'Ulgu", "min": 36, "max": 64, "tier": 3, "desc": "Pénétration absolue", "classes": ["khainite"]}
    ]
}

ARMORS_BY_TIER = {
    1: [
        {"name": "Cotte de mailles de l'Empire", "def": 3, "tier": 1, "desc": "Protections en fer standard", "classes": ["empire"]},
        {"name": "Cuir de Vétéran du Reik", "def": 2, "tier": 1, "desc": "Souple et renforcé aux épaules", "classes": ["empire"]},
        {"name": "Tunique de Cuir Renforcé", "def": 2, "tier": 1, "desc": "Légère et adaptée au combat", "classes": ["slayer", "khainite"]},
        {"name": "Peau de Sanglier Sauvage", "def": 3, "tier": 1, "desc": "Épaisse et brutale", "classes": ["slayer"]},
        {"name": "Robe Bénie de Sigmar", "def": 4, "tier": 1, "desc": "Tissu sacralisé par la foi", "classes": ["sigmar"]},
        {"name": "Soutane du Penitent", "def": 3, "tier": 1, "desc": "Renforcée par des plaques d'acier", "classes": ["sigmar"]},
        {"name": "Manteau de Soie d'Ulthuan", "def": 2, "tier": 1, "desc": "Élégance et légèreté elfique", "classes": ["elfe"]},
        {"name": "Cotte de Mailles d'Avelorn", "def": 3, "tier": 1, "desc": "Tressée par les artisans elfes", "classes": ["elfe"]},
        {"name": "Robe de Cendres", "def": 1, "tier": 1, "desc": "Tissu chargé d'énergie arcanique", "classes": ["bright_wizard"]},
        {"name": "Manteau de Flamme Mineure", "def": 2, "tier": 1, "desc": "Isole de la chaleur et des coups", "classes": ["bright_wizard"]},
        {"name": "Tunique des Ombres d'Ulgu", "def": 2, "tier": 1, "desc": "Discrète et imperméable", "classes": ["khainite"]}
    ],
    2: [
        {"name": "Harnois Complet du Reikland", "def": 7, "tier": 2, "desc": "Acier trempé d'Altdorf", "classes": ["empire"]},
        {"name": "Armure du Garde Noir", "def": 8, "tier": 2, "desc": "Plaques lourdes et solides", "classes": ["empire"]},
        {"name": "Peau de Troll Tannée", "def": 5, "tier": 2, "desc": "Résistance brute et cuir épais", "classes": ["slayer"]},
        {"name": "Sangles Runiques de Karak", "def": 6, "tier": 2, "desc": "Gravées de protections naines", "classes": ["slayer"]},
        {"name": "Armure de Plaque du Marteau", "def": 8, "tier": 2, "desc": "Forgée pour les Prêtres-Guerriers", "classes": ["sigmar"]},
        {"name": "Cuirasse de Ferveur Sacrée", "def": 9, "tier": 2, "desc": "Bénie contre les attaques du Chaos", "classes": ["sigmar"]},
        {"name": "Cotte d'Ithilmar Flamboyante", "def": 5, "tier": 2, "desc": "Métal elfique extrêmement léger", "classes": ["elfe"]},
        {"name": "Armure des Patrouilleurs d'Avelorn", "def": 6, "tier": 2, "desc": "Camouflage et acier souple", "classes": ["elfe"]},
        {"name": "Robe de Pyromancien", "def": 3, "tier": 2, "desc": "Barrière magique de chaleur", "classes": ["bright_wizard"]},
        {"name": "Toge d'Incinération D'Aqshy", "def": 4, "tier": 2, "desc": "Tissée dans les braises magiques", "classes": ["bright_wizard"]},
        {"name": "Cuirasse d'Ébonite Khainite", "def": 5, "tier": 2, "desc": "Protection sombre et silencieuse", "classes": ["khainite"]},
        {"name": "Manteau du Tueur de l'Ombre", "def": 6, "tier": 2, "desc": "Dévie les lames ennemies", "classes": ["khainite"]}
    ],
    3: [
        {"name": "Armure d'Orichalque du Reik", "def": 14, "tier": 3, "desc": "Protection légendaire des comtes", "classes": ["empire"]},
        {"name": "Harnois Impérial de Karl Franz", "def": 16, "tier": 3, "desc": "La meilleure armure d'Altdorf", "classes": ["empire"]},
        {"name": "Rune Majeure d'Invulnérabilité", "def": 10, "tier": 3, "desc": "Gravée directement sur la chair", "classes": ["slayer"]},
        {"name": "Peau de Dragon Ancien", "def": 12, "tier": 3, "desc": "Écailles impénétrables", "classes": ["slayer"]},
        {"name": "Plaque Céleste d'Azyr", "def": 15, "tier": 3, "desc": "Forgée sous les éclairs célestes", "classes": ["sigmar"]},
        {"name": "Armure Divine du Grand Théogoniste", "def": 17, "tier": 3, "desc": "Halo de protection absolue", "classes": ["sigmar"]},
        {"name": "Armure Stellaire d'Avelorn", "def": 11, "tier": 3, "desc": "Forgée en Ithilmar pur", "classes": ["elfe"]},
        {"name": "Plaque Céleste des Hauts-Elfes", "def": 13, "tier": 3, "desc": "Bénie par les Dieux d'Ulthuan", "classes": ["elfe"]},
        {"name": "Cape de Tempête d'Aqshy", "def": 8, "tier": 3, "desc": "Absorbe la magie et les dégâts", "classes": ["bright_wizard"]},
        {"name": "Robe du Cataclysme Flamboyant", "def": 10, "tier": 3, "desc": "Entourée d'un bouclier de feu", "classes": ["bright_wizard"]},
        {"name": "Voile de Mort de Har Ganeth", "def": 10, "tier": 3, "desc": "Baigné dans le sang de Khaine", "classes": ["khainite"]},
        {"name": "Armure de Sang du Grand Assassin", "def": 12, "tier": 3, "desc": "Rend presque intouchable dans le noir", "classes": ["khainite"]}
    ]
}

MONSTERS_POOL = {
    1: [
        {"name": "Guerrier Skaven", "hp": 25, "max_hp": 25, "atk_min": 5, "atk_max": 9, "xp": 25},
        {"name": "Grot des Cavernes", "hp": 20, "max_hp": 20, "atk_min": 6, "atk_max": 11, "xp": 20},
        {"name": "Zombie de Sylvanie", "hp": 35, "max_hp": 35, "atk_min": 3, "atk_max": 7, "xp": 22},
        {"name": "Gore-Norse Sauvage", "hp": 30, "max_hp": 30, "atk_min": 7, "atk_max": 10, "xp": 28},
        {"name": "Loup des Ombres", "hp": 22, "max_hp": 22, "atk_min": 8, "atk_max": 12, "xp": 24},
        {"name": "Cultiste de Nurgle", "hp": 28, "max_hp": 28, "atk_min": 4, "atk_max": 9, "xp": 23},
        {"name": "Unigor des Bois", "hp": 26, "max_hp": 26, "atk_min": 6, "atk_max": 10, "xp": 25},
        {"name": "Chauve-souris Géante", "hp": 18, "max_hp": 18, "atk_min": 7, "atk_max": 13, "xp": 21},
        {"name": "Nuée de Rats Pesteux", "hp": 15, "max_hp": 15, "atk_min": 4, "atk_max": 8, "xp": 18},
        {"name": "Garde Squelette Décrépit", "hp": 32, "max_hp": 32, "atk_min": 5, "atk_max": 9, "xp": 26}
    ],
    2: [
        {"name": "Boy Orc Noir", "hp": 55, "max_hp": 55, "atk_min": 9, "atk_max": 15, "xp": 50},
        {"name": "Guerrier du Chaos", "hp": 65, "max_hp": 65, "atk_min": 8, "atk_max": 14, "xp": 55},
        {"name": "Squelette de la Tombe", "hp": 45, "max_hp": 45, "atk_min": 11, "atk_max": 16, "xp": 48},
        {"name": "Vermine de Choc Skaven", "hp": 50, "max_hp": 50, "atk_min": 10, "atk_max": 18, "xp": 52},
        {"name": "Goule des Cryptes", "hp": 40, "max_hp": 40, "atk_min": 12, "atk_max": 19, "xp": 46},
        {"name": "Homme-Bête Gor", "hp": 60, "max_hp": 60, "atk_min": 9, "atk_max": 16, "xp": 53},
        {"name": "Chien du Chaos", "hp": 42, "max_hp": 42, "atk_min": 13, "atk_max": 17, "xp": 47},
        {"name": "Garde des Cryptes", "hp": 58, "max_hp": 58, "atk_min": 10, "atk_max": 15, "xp": 51},
        {"name": "Goblinoïde Fana-Boulet", "hp": 38, "max_hp": 38, "atk_min": 14, "atk_max": 22, "xp": 54},
        {"name": "Moine de la Peste Skaven", "hp": 48, "max_hp": 48, "atk_min": 11, "atk_max": 18, "xp": 49}
    ],
    3: [
        {"name": "Sanguinaire de Khorne", "hp": 90, "max_hp": 90, "atk_min": 15, "atk_max": 24, "xp": 90},
        {"name": "Démonette de Slaanesh", "hp": 75, "max_hp": 75, "atk_min": 18, "atk_max": 28, "xp": 88},
        {"name": "Porte-Peste de Nurgle", "hp": 115, "max_hp": 115, "atk_min": 12, "atk_max": 20, "xp": 95},
        {"name": "Revenant des Cryptes", "hp": 85, "max_hp": 85, "atk_min": 16, "atk_max": 25, "xp": 92},
        {"name": "Horreur Bleue de Tzeentch", "hp": 80, "max_hp": 80, "atk_min": 14, "atk_max": 27, "xp": 89},
        {"name": "Minotaure du Chaos", "hp": 110, "max_hp": 110, "atk_min": 17, "atk_max": 26, "xp": 98},
        {"name": "Orc Sauvage Costaud", "hp": 95, "max_hp": 95, "atk_min": 16, "atk_max": 23, "xp": 91},
        {"name": "Cavalier de la Mort Sylvanien", "hp": 88, "max_hp": 88, "atk_min": 15, "atk_max": 25, "xp": 93},
        {"name": "Centigor Déchaîné", "hp": 100, "max_hp": 100, "atk_min": 14, "atk_max": 22, "xp": 94},
        {"name": "Gourmand Ogor", "hp": 120, "max_hp": 120, "atk_min": 13, "atk_max": 21, "xp": 96}
    ],
    4: [
        {"name": "Rat-Ogre Muté", "hp": 160, "max_hp": 160, "atk_min": 22, "atk_max": 35, "xp": 150},
        {"name": "Ogre des Montagnes", "hp": 180, "max_hp": 180, "atk_min": 20, "atk_max": 32, "xp": 155},
        {"name": "Troll d'Eau fétide", "hp": 200, "max_hp": 200, "atk_min": 18, "atk_max": 30, "xp": 160},
        {"name": "Horreur Rose de Tzeentch", "hp": 140, "max_hp": 140, "atk_min": 25, "atk_max": 40, "xp": 165},
        {"name": "Varghulf Enragé", "hp": 175, "max_hp": 175, "atk_min": 24, "atk_max": 38, "xp": 158},
        {"name": "Araignée Géante des Forêts", "hp": 150, "max_hp": 150, "atk_min": 21, "atk_max": 36, "xp": 152},
        {"name": "Elu du Chaos Éternel", "hp": 190, "max_hp": 190, "atk_min": 23, "atk_max": 34, "xp": 162},
        {"name": "Vargheist Ailé", "hp": 145, "max_hp": 145, "atk_min": 26, "atk_max": 42, "xp": 157},
        {"name": "Cygor Aveugle", "hp": 210, "max_hp": 210, "atk_min": 19, "atk_max": 31, "xp": 168},
        {"name": "Raza-Gore Écorché", "hp": 165, "max_hp": 165, "atk_min": 22, "atk_max": 37, "xp": 154}
    ],
    5: [
        {"name": "Buveur de Sang de Khorne", "hp": 280, "max_hp": 280, "atk_min": 35, "atk_max": 55, "xp": 300},
        {"name": "Grand Immonde de Nurgle", "hp": 350, "max_hp": 350, "atk_min": 28, "atk_max": 48, "xp": 320},
        {"name": "Duc du Changement", "hp": 250, "max_hp": 250, "atk_min": 40, "atk_max": 65, "xp": 310},
        {"name": "Seigneur de la Nuée Skaven", "hp": 300, "max_hp": 300, "atk_min": 32, "atk_max": 58, "xp": 305},
        {"name": "Dragon-Ogre Shaggoth", "hp": 320, "max_hp": 320, "atk_min": 38, "atk_max": 60, "xp": 330},
        {"name": "Gardien des Secrets de Slaanesh", "hp": 270, "max_hp": 270, "atk_min": 42, "atk_max": 62, "xp": 315},
        {"name": "Wyrm de Givre des Désolations", "hp": 340, "max_hp": 340, "atk_min": 36, "atk_max": 54, "xp": 325},
        {"name": "Terreur des Abîmes Vampirique", "hp": 310, "max_hp": 310, "atk_min": 34, "atk_max": 56, "xp": 318},
        {"name": "Jabberslythe Abominable", "hp": 330, "max_hp": 330, "atk_min": 30, "atk_max": 50, "xp": 312},
        {"name": "Arachnarok Venimeuse", "hp": 360, "max_hp": 360, "atk_min": 29, "atk_max": 46, "xp": 335}
    ]
}

BOSSES_POOL = [
    {"name": "👑 Buveur de Sang de Khorne (Boss)", "hp": 350, "max_hp": 350, "atk_min": 25, "atk_max": 45, "xp": 300, "gold_reward": 150},
    {"name": "👑 Grand Immonde de Nurgle (Boss)", "hp": 450, "max_hp": 450, "atk_min": 18, "atk_max": 35, "xp": 350, "gold_reward": 180},
    {"name": "👑 Duc du Changement de Tzeentch (Boss)", "hp": 300, "max_hp": 300, "atk_min": 30, "atk_max": 50, "xp": 320, "gold_reward": 160},
    {"name": "👑 Gardien des Secrets de Slaanesh (Boss)", "hp": 320, "max_hp": 320, "atk_min": 28, "atk_max": 48, "xp": 330, "gold_reward": 170},
    {"name": "👑 Prophète Gris Skaven (Boss)", "hp": 280, "max_hp": 280, "atk_min": 22, "atk_max": 42, "xp": 280, "gold_reward": 140}
]
