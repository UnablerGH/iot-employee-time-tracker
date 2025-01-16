import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"

# Function to test employee entry
def test_entry(uid):
    response = requests.post(f"{BASE_URL}/entry/{uid}")
    print(f"POST /entry/{uid} response:")
    if response.status_code == 201:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error: {response.status_code}")
    print()

# Function to test employee leave
def test_leave(uid):
    time.sleep(2)  # Simulate a short delay to allow some "work time"
    response = requests.post(f"{BASE_URL}/leave/{uid}")
    print(f"POST /leave/{uid} response:")
    if response.status_code == 201:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error: {response.status_code}")
    print()

# Function to fetch logs
def test_get_logs():
    response = requests.get(f"{BASE_URL}/logs")
    print("GET /logs response:")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error: {response.status_code}")
    print()

# Function to fetch daily summary
def test_daily_summary():
    response = requests.get(f"{BASE_URL}/daily_summary")
    print("GET /daily_summary response:")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error: {response.status_code}")
    print()

# Simulate a workday for all employees
def simulate_workday():
    uids = ["1234567890", "0987654321", "1839402942"]
    for uid in uids:
        test_entry(uid)  # Employee enters
        test_leave(uid)  # Employee leaves

# Run the tests
def run_tests():
    print("Simulating workday...\n")
    simulate_workday()
    
    print("Fetching logs...\n")
    test_get_logs()

    print("Fetching daily summary...\n")
    test_daily_summary()

if __name__ == "__main__":
    run_tests()
