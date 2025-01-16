import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def check_action(uid):
    """Determine if the UID represents an entry or leave."""
    # Get the latest entry for the UID
    response = requests.get(f"{BASE_URL}/logs")
    if response.status_code == 200:
        logs = response.json()
        # Find the latest log for the UID
        logs = [log for log in logs if log['UID'] == uid]
        if logs:
            latest_log = sorted(logs, key=lambda x: x['id'], reverse=True)[0]
            # If leave_time is null, it's a leave action
            if not latest_log['leave_time']:
                return "leave"
        return "entry"
    else:
        print(f"Error fetching logs: {response.status_code}")
        return None

def send_request(uid, action):
    """Send the appropriate request to the API based on the action."""
    if action == "entry":
        response = requests.post(f"{BASE_URL}/entry/{uid}")
        if response.status_code == 201:
            print(f"Entry logged for UID {uid}.")
        else:
            print(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
    elif action == "leave":
        response = requests.post(f"{BASE_URL}/leave/{uid}")
        if response.status_code == 201:
            print(f"Leave logged for UID {uid}.")
        else:
            print(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")

def rfid_terminal():
    """Simulate the RFID card terminal."""
    print("RFID Terminal Simulator. Type 'exit' to quit.")
    while True:
        uid = input("Scan RFID card (type UID): ").strip()
        if uid.lower() == "exit":
            print("Exiting RFID Terminal Simulator.")
            break
        if not uid:
            print("UID cannot be empty. Try again.")
            continue
        action = check_action(uid)
        if action:
            send_request(uid, action)
        else:
            print(f"Unable to determine action for UID {uid}. Check the API or logs.")

if __name__ == "__main__":
    rfid_terminal()
