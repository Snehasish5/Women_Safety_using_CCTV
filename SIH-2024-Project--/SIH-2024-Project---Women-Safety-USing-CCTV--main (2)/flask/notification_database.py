import sqlite3
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# Function to create notifications table
def create_notifications_table():
    conn = sqlite3.connect('notification_uploads.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        timestamp TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to store notifications
def store_notification(message):
    conn = sqlite3.connect('notification_uploads.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
    c.execute("INSERT INTO notifications (message, timestamp) VALUES (?, ?)", (message, timestamp))
    conn.commit()
    conn.close()

@app.route('/notifications', methods=['GET'])
def get_notifications():
    conn = sqlite3.connect('notification_uploads.db')
    c = conn.cursor()
    c.execute("SELECT message, timestamp FROM notifications ORDER BY timestamp DESC")
    notifications = c.fetchall()
    conn.close()
    return jsonify(notifications)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Simulated Event Detection
def detect_event(detected_genders):
    if 'Female' in detected_genders:
        num_females = detected_genders.count('Female')
        num_males = detected_genders.count('Male')
        if num_females == 1 and num_males == 0:
            store_notification('Lone woman detected')
        elif num_females > 0 and num_males > num_females:
            store_notification('Woman surrounded by men')

if __name__ == "__main__":
    create_notifications_table()
    app.run(debug=True)