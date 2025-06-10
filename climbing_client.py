import socket
import json

SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 5001 

def send_climbing_alert(payload: dict):
    """Send a climbing detection alert to the server."""
    print(f"🔄 Bağlantı kuruluyor: {SERVER_HOST}:{SERVER_PORT}")
    print(f"📦 Gönderilecek data: {payload}")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_HOST, SERVER_PORT))
            message = json.dumps(payload).encode('utf-8')
            sock.sendall(message)
            print("✅ Bildirim başarıyla gönderildi!")
    except Exception as e:
        print(f"❌ Bildirim gönderilemedi: {e}")
        print(f"❌ Hata detayı: {type(e).__name__}")