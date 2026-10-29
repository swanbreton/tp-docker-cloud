import socket
import signal
import sys
import os

# Gestion propre du signal SIGTERM pour arrêt sans délai du conteneur Docker
signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "9000"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

print(f"Game Server TCP listening on {host}:{port}...", flush=True)

while True:
    try:
        c, addr = s.accept()
        c.send(b"Game Server Ok\n")
        c.close()
    except Exception:
        break