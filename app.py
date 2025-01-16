from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import time
import threading

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This makes rows return as dictionaries
    return conn

# Initialize database: Create tables and insert sample data if necessary
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop tables for a fresh start
    cursor.execute("DROP TABLE IF EXISTS employees")
    cursor.execute("DROP TABLE IF EXISTS entries")

    # Create employees table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        UID TEXT NOT NULL UNIQUE
    )
    ''')

    # Create entries table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        UID TEXT NOT NULL,
        entry_time TEXT NOT NULL,
        leave_time TEXT,
        FOREIGN KEY (UID) REFERENCES employees (UID)
    )
    ''')

    # Insert sample data into employees table
    sample_data = [('1234567890',), ('0987654321',), ('1839402942',)]
    cursor.executemany("INSERT INTO employees (UID) VALUES (?)", sample_data)
    
    conn.commit()
    conn.close()

# Endpoint to track employee entry by UID
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

# Endpoint to track employee leave by UID
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

# Endpoint to get total time for all employees
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

# Endpoint to fetch all logs
@app.route('/logs', methods=['GET'])
def get_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(logs), 200

# Simulate a workday
def simulate_workday():
    time.sleep(2)  # Simulate a short delay before starting
    uids = ['1234567890', '0987654321', '1839402942']
    for uid in uids:
        request.post(f"http://127.0.0.1:5000/entry/{uid}")
        time.sleep(5)  # Simulate 5 seconds of work
        request.post(f"http://127.0.0.1:5000/leave/{uid}")

# Initialize database
initialize_database()

if __name__ == '__main__':
    # Start simulation in a separate thread
    threading.Thread(target=simulate_workday, daemon=True).start()
    app.run(debug=True)
