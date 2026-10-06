import signal, sys
from flask import Flask
app = Flask(__name__)
signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))
@app.route("/api")
def api(): return {"status": "ok"}
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)