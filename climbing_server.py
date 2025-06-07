import socket
import json
import threading
from tkinter import Tk, Listbox, END

HOST = '0.0.0.0'
PORT = 5001

# ─ GUI Setup ─
root = Tk()
root.title("🚨 Climbing Alert Server")
listbox = Listbox(root, width=80, height=20)
listbox.pack(padx=10, pady=10)

def handle_client(conn, addr):
    with conn:
        data = conn.recv(1024)
        if data:
            try:
                alert = json.loads(data.decode('utf-8'))
                msg = f"[{alert['timestamp']}] 🚀 ID {alert['id']} climbed (frame {alert['frame']})"
                print(msg)
                listbox.insert(END, msg)
                listbox.yview(END)
            except Exception as e:
                print(f"[⚠️] Invalid data: {e}")

def socket_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 🛠 Prevent "Address already in use"
        s.bind((HOST, PORT))
        s.listen()
        print(f"🖥️ Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# ─ Main ─
threading.Thread(target=socket_listener, daemon=True).start()
root.mainloop()
