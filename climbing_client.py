import socket
import json

SERVER_HOST = '127.0.0.1'  # localhost for testing
SERVER_PORT = 5001           # match this on both client & server

def send_climbing_alert(payload: dict):
    """Send a climbing detection alert to the server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_HOST, SERVER_PORT))
            sock.sendall(json.dumps(payload).encode('utf-8'))
    except Exception as e:
        print(f"[⚠️] Failed to send alert to server: {e}")
