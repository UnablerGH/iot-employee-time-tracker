import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def get_latest_entries(uid, n):
    """Fetch the latest `n` entries for the given UID. If n is -1, fetch all."""
    response = requests.get(f"{BASE_URL}/logs")
    if response.status_code == 200:
        logs = response.json()
        # Filter logs for the given UID and sort by ID (latest first)
        user_logs = sorted([log for log in logs if log["UID"] == uid], key=lambda x: x["id"], reverse=True)
        if n == -1:
            return user_logs  # Return all logs
        return user_logs[:n]
    else:
        print(f"Error fetching logs: {response.status_code}")
        return []

def calculate_time_spent(log):
    """Calculate time spent in the office for a single log."""
    if log["entry_time"] and log["leave_time"]:
        entry_time = datetime.strptime(log["entry_time"], "%Y-%m-%d %H:%M:%S")
        leave_time = datetime.strptime(log["leave_time"], "%Y-%m-%d %H:%M:%S")
        return leave_time - entry_time
    return None

def view_employee_logs():
    """View the latest `n` entries for an employee."""
    uid = input("Enter employee UID: ").strip()
    if not uid:
        print("UID cannot be empty!")
        return

    try:
        n = int(input("How many latest entries do you want to view? (Enter -1 to see all): "))
        if n == 0:
            print("Please enter a positive number or -1 for all entries.")
            return
    except ValueError:
        print("Invalid number entered.")
        return

    logs = get_latest_entries(uid, n)
    if logs:
        print(f"\nLatest {'all' if n == -1 else n} entries for UID {uid}:")
        for i, log in enumerate(logs, start=1):
            time_spent = calculate_time_spent(log)
            print(f"{i}. Entry: {log['entry_time']}, Leave: {log['leave_time']}, Time Spent: {time_spent or 'Still inside'}")
    else:
        print(f"No logs found for UID {uid}.")

def view_daily_summary():
    """View the daily summary for all employees."""
    response = requests.get(f"{BASE_URL}/daily_summary")
    if response.status_code == 200:
        summary = response.json()
        print("\nDaily Summary:")
        for record in summary:
            print(f"UID: {record['UID']}, Total Time: {record['total_time']}")
    else:
        print(f"Error fetching daily summary: {response.status_code}")

def view_all_logs():
    """View all logs."""
    response = requests.get(f"{BASE_URL}/logs")
    if response.status_code == 200:
        logs = response.json()
        print("\nAll Logs:")
        for log in logs:
            print(log)
    else:
        print(f"Error fetching logs: {response.status_code}")

def admin_terminal():
    """Interactive terminal for admin actions."""
    while True:
        print("\nAdmin Panel")
        print("1. View employee entry times and time spent")
        print("2. View daily summary")
        print("3. View all logs")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_employee_logs()
        elif choice == "2":
            view_daily_summary()
        elif choice == "3":
            view_all_logs()
        elif choice == "4":
            print("Exiting Admin Panel.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    admin_terminal()
