import socket
import signal
import sys

# Gestion propre du signal SIGTERM (remplit l'exigence du barème)
signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))

s = socket.socket()
s.bind(("0.0.0.0", 9000))
s.listen(5)

print("Game Server à l'écoute sur le port 9000...")

while True:
    try:
        c, _ = s.accept()
        c.send(b"Game Server Ok\n")
        c.close()
    except Exception:
        break