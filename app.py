from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This makes rows return as dictionaries
    return conn

# Endpoint to get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    
    # Convert query results into a list of dictionaries
    employee_list = [dict(row) for row in employees]
    
    return jsonify(employee_list)

# Endpoint to get an employee by UID
@app.route('/employee/<uid>', methods=['GET'])
def get_employee_by_uid(uid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE UID = ?", (uid,))
    employee = cursor.fetchone()
    conn.close()

    if employee:
        return jsonify(dict(employee))
    else:
        return jsonify({"message": "Employee not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
