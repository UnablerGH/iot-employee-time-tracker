import requests
import json

# Base URL of the Flask API
BASE_URL = "http://127.0.0.1:5000"

# Test GET /employees - Fetch all employees
def test_get_employees():
    response = requests.get(f"{BASE_URL}/employees")
    print("GET /employees response:")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed: {response.status_code}")
    print()

# Test GET /employee/<uid> - Fetch employee by UID
def test_get_employee_by_uid(uid):
    response = requests.get(f"{BASE_URL}/employee/{uid}")
    print(f"GET /employee/{uid} response:")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed: {response.status_code}")
    print()

# Test POST /employee - Add a new employee
def test_add_employee(uid):
    response = requests.post(
        f"{BASE_URL}/employee", 
        json={"UID": uid}
    )
    print(f"POST /employee response (UID: {uid}):")
    if response.status_code == 201:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed: {response.status_code}")
    print()

# Run tests
def run_tests():
    test_get_employees()  # Get all employees

    test_get_employee_by_uid("1234567890")  # Get employee by UID
    test_get_employee_by_uid("0987654321")  # Get another employee by UID
    test_get_employee_by_uid("nonexistent_uid")  # Try to get a non-existing employee by UID

    test_add_employee("1112233445")  # Add a new employee with a unique UID
    test_add_employee("1234567890")  # Try to add an employee with an existing UID (should fail)

    test_get_employees()  # Get all employees again after adding new one

if __name__ == '__main__':
    run_tests()
