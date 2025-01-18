from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import time
import threading
import requests

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS employees")
    cursor.execute("DROP TABLE IF EXISTS entries")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        UID TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        UID TEXT NOT NULL,
        entry_time TEXT NOT NULL,
        leave_time TEXT,
        FOREIGN KEY (UID) REFERENCES employees (UID)
    )
    ''')

    sample_data = [('1234567890',), ('0987654321',), ('1839402942',)]
    cursor.executemany("INSERT INTO employees (UID) VALUES (?)", sample_data)
    
    conn.commit()
    conn.close()

@app.route('/add_employee/<uid>', methods=['POST'])
def add_employee(uid):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO employees (UID) VALUES (?)", (uid,))
        conn.commit()
        message = f"Employee with UID {uid} successfully added."
        status_code = 201
    except sqlite3.IntegrityError:
        message = f"Employee with UID {uid} already exists."
        status_code = 400
    finally:
        conn.close()

    return jsonify({"message": message}), status_code

@app.route('/entry/<uid>', methods=['POST'])
def track_entry(uid):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM employees WHERE UID = ?", (uid,))
    employee = cursor.fetchone()
    
    if employee:
        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO entries (UID, entry_time) VALUES (?, ?)", (uid, entry_time))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Entry logged for UID {uid} at {entry_time}"}), 201
    else:
        conn.close()
        return jsonify({"message": "Employee not found"}), 404

@app.route('/leave/<uid>', methods=['POST'])
def track_leave(uid):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM entries WHERE UID = ? AND leave_time IS NULL ORDER BY id DESC LIMIT 1", (uid,))
    entry = cursor.fetchone()
    
    if entry:
        leave_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE entries SET leave_time = ? WHERE id = ?", (leave_time, entry['id']))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Leave logged for UID {uid} at {leave_time}"}), 201
    else:
        conn.close()
        return jsonify({"message": "No active entry record found for this employee"}), 404

@app.route('/daily_summary', methods=['GET'])
def daily_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT UID, SUM(strftime('%s', leave_time) - strftime('%s', entry_time)) as total_time
    FROM entries
    WHERE leave_time IS NOT NULL
    GROUP BY UID
    ''')
    summary = [{"UID": row["UID"], "total_time": f"{row['total_time']} seconds"} for row in cursor.fetchall()]
    conn.close()
    return jsonify(summary), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(logs), 200




if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
