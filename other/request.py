import socket
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8765        # The port used by the server

def req(text):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(bytes(text, "utf8"))
    s.close()

steam_id = sys.argv[1]
achievement = sys.argv[2]

req(f"{steam_id},{achievement}")

