import signal
import sys
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Interception du signal SIGTERM
signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))

monster_hp = 100

# Middleware CORS pour autoriser le Frontend (port 8081)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route("/api", methods=["GET", "OPTIONS"])
def api():
    return jsonify({"status": "ok"})

@app.route("/api/attack", methods=["POST", "OPTIONS"])
def attack():
    global monster_hp
    damage = random.randint(10, 25)
    monster_hp = max(0, monster_hp - damage)
    
    if monster_hp == 0:
        monster_hp = 100
        return jsonify({
            "damage": damage,
            "hp": 0,
            "message": "Monstre terrassé ! Un nouveau monstre apparaît !"
        })
    
    return jsonify({
        "damage": damage,
        "hp": monster_hp,
        "message": f"Attaque réussie ! -{damage} HP infligés."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)