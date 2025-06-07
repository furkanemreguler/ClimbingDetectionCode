import smtplib
from email.mime.text import MIMEText
import mysql.connector
from datetime import datetime
import os

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
SECURITY_EMAIL = os.getenv("SECURITY_EMAIL", "security-team@example.com")
SENDER_EMAIL   = os.getenv("SENDER_EMAIL", "youremail@gmail.com")
SENDER_PASS    = os.getenv("SENDER_PASS", "your_app_password")

# MySQL config - Docker-friendly
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", 3307)),
    "user": os.getenv("MYSQL_USER", "climbing_project"),
    "password": os.getenv("MYSQL_PASSWORD", "smartcampus"),
    "database": os.getenv("MYSQL_DATABASE", "climbing_system")
}


# ─── DATABASE FUNCTIONS ───────────────────────────────────────────────────────
def init_db():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS climbing_events (
                id INT,
                frame INT,
                latency_ms FLOAT,
                timestamp VARCHAR(255)
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ MySQL DB initialized.")
    except Exception as e:
        print(f"[DB Error] {e}")

def store_event_to_db(event):
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO climbing_events (id, frame, latency_ms, timestamp)
            VALUES (%s, %s, %s, %s)
        ''', (event['id'], event['frame'], event['latency_ms'], event['timestamp']))
        conn.commit()
        conn.close()
        print("🗃️ Event stored in MySQL.")
    except Exception as e:
        print(f"[⚠️ MySQL Error] {e}")

# ─── EMAIL FUNCTION ───────────────────────────────────────────────────────────
def send_email_alert(event):
    body = f"""
🚨 CLIMBING DETECTED
--------------------
ID:        {event['id']}
Frame:     {event['frame']}
Latency:   {event['latency_ms']} ms
Time:      {event['timestamp']}
    """
    msg = MIMEText(body)
    msg['Subject'] = f"[SECURITY] Climbing Detected - ID {event['id']}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = SECURITY_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.send_message(msg)
        print("📧 Email alert sent to security.")
    except Exception as e:
        print(f"[⚠️ Email Error] {e}")