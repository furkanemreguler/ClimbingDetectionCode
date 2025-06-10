import socket
import json
import threading
from tkinter import Tk, Text, Scrollbar, END
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5001

# ─ GUI Setup ─
root = Tk()
root.title("🚨 Climbing Alert Server")
root.geometry("800x600")
root.attributes('-topmost', True)

# Text widget kullan (Listbox yerine)
scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")

text_area = Text(root, width=80, height=30, yscrollcommand=scrollbar.set)
text_area.pack(padx=10, pady=10, fill="both", expand=True)
scrollbar.config(command=text_area.yview)

def add_message_to_gui(message):
    """GUI'ye mesaj ekle"""
    text_area.insert(END, message + "\n")
    text_area.see(END)  # En sona scroll
    root.update()  # Zorla güncelle
    print(f"✅ GUI'ye eklendi: {message}")

def handle_client(conn, addr):
    with conn:
        try:
            data = conn.recv(1024)
            if data:
                alert = json.loads(data.decode('utf-8'))
                msg = f"[{alert.get('timestamp', datetime.now().strftime('%H:%M:%S'))}] 🚀 ID {alert.get('id', '?')} climbed (frame {alert.get('frame', '?')}) - {alert.get('latency_ms', '?')}ms"
                add_message_to_gui(msg)
        except Exception as e:
            error_msg = f"[ERROR] {datetime.now().strftime('%H:%M:%S')} - Hata: {e}"
            add_message_to_gui(error_msg)

def socket_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"🖥️ Server listening on {HOST}:{PORT}")
        
        # Test mesajı
        add_message_to_gui("🎯 Server başlatıldı - Test mesajı")
        
        while True:
            try:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except Exception as e:
                print(f"Socket error: {e}")

# ─ Main ─
if __name__ == "__main__":
    threading.Thread(target=socket_listener, daemon=True).start()
    root.mainloop()