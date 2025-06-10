from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import socket
import json
import threading
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'climbing_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Mesajları sakla
messages = []

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚨 Climbing Alert Server</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: white; }
            .container { max-width: 1000px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 20px; }
            .messages { 
                border: 2px solid #333; 
                height: 500px; 
                overflow-y: auto; 
                padding: 15px; 
                background: #2a2a2a;
                border-radius: 10px;
                font-family: monospace;
            }
            .message { 
                margin: 5px 0; 
                padding: 8px;
                background: #3a3a3a;
                border-radius: 5px;
                border-left: 4px solid #4CAF50;
            }
            .status { 
                text-align: center; 
                margin: 10px 0; 
                color: #4CAF50;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚨 Climbing Detection Alert Server</h1>
                <div class="status" id="status">🟢 Bağlı ve Dinliyor</div>
            </div>
            
            <div class="messages" id="messages">
                {% for msg in messages %}
                    <div class="message">{{ msg }}</div>
                {% endfor %}
            </div>
        </div>

        <script>
            const socket = io();
            
            socket.on('new_message', function(data) {
                const messages = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message';
                messageDiv.textContent = data.message;
                messages.appendChild(messageDiv);
                messages.scrollTop = messages.scrollHeight;
            });
            
            socket.on('connect', function() {
                document.getElementById('status').innerHTML = '🟢 Bağlı ve Dinliyor';
            });
            
            socket.on('disconnect', function() {
                document.getElementById('status').innerHTML = '🔴 Bağlantı Kesildi';
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html, messages=messages)

def add_message(msg):
    """Mesaj ekle ve websocket ile gönder"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    full_msg = f"[{timestamp}] {msg}"
    messages.append(full_msg)
    
    # En son 100 mesajı tut
    if len(messages) > 100:
        messages.pop(0)
    
    # WebSocket ile realtime gönder
    socketio.emit('new_message', {'message': full_msg})
    print(f"✅ Web GUI'ye eklendi: {full_msg}")

def handle_client(conn, addr):
    """Socket client'ları handle et"""
    with conn:
        try:
            data = conn.recv(1024)
            if data:
                alert = json.loads(data.decode('utf-8'))
                msg = f"🚀 ID {alert.get('id', '?')} climbed (frame {alert.get('frame', '?')}) - {alert.get('latency_ms', '?')}ms"
                add_message(msg)
        except Exception as e:
            add_message(f"❌ Hata: {e}")

def socket_listener():
    """Socket server başlat"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 5001))
        s.listen()
        print(f"🖥️ Socket server listening on 0.0.0.0:5001")
        
        add_message("🎯 Socket server başlatıldı")
        
        while True:
            try:
                conn, addr = s.accept()
                print(f"Socket bağlantısı: {addr}")
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except Exception as e:
                print(f"Socket error: {e}")

if __name__ == "__main__":
    # Test mesajları
    add_message("🚀 Web server başlatıldı")
    add_message("📡 Port 5001'de socket dinliyor")
    add_message("🌐 Web arayüzü: http://localhost:5002")
    
    # Socket listener'ı başlat
    threading.Thread(target=socket_listener, daemon=True).start()
    
    # Web server'ı başlat
    print("🌐 Web GUI açılıyor: http://localhost:5002")
    socketio.run(app, host='127.0.0.1', port=5002, debug=False)