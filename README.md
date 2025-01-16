# IoT Employee Time Tracker

This is an IoT-based employee time tracking system designed to monitor and record office attendance using RFID cards. The system allows employees to clock in and out using their unique RFID UID, and it tracks key statistics like attendance percentage, working hours, and number of daily entries.

The backend of the system is powered by Flask and uses a local database to store user information and attendance records. The frontend is currently not implemented, as this is a basic version focusing on the backend functionalities.

## Features

- **RFID-based Authentication**: Employees are identified via RFID cards. Each card has a unique UID, and only recognized cards can authorize entry.
  
- **Time Tracking**: The system keeps track of entry and exit times for each employee and calculates their working hours.

- **Attendance Statistics**: For each employee, the system maintains:
  - Attendance percentage (based on working days).
  - Total working hours.
  - Daily entries (number of times an employee enters the office).

- **Fixed Work Schedule**: Each employee has a predefined work schedule, which the system uses to compare against actual attendance and working hours.

- **Manual User Management**: New users can be added manually by an admin. Only authorized cards (with recognized UID numbers) are allowed.

## Project Scope

- **User Registration**: Users are added manually into the database, and each user is linked to a unique RFID card number.
  
- **Authentication**: Only employees with recognized RFID UIDs can gain access. Cards not recognized by the system will not authorize access.

- **Data Storage**: The system utilizes a local database (SQLite or similar) to store user details, attendance records, and statistics.

## Requirements

- **Backend**: Flask (Python-based framework)
- **Database**: Local SQLite database (or similar lightweight database)
- **RFID Reader**: Hardware component to read RFID cards and pass UID data to the system

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/iot-employee-time-tracker.git
cd iot-employee-time-tracker
```

### 2. Create the python virtual environment and install required libraties

   ```bash
   python -m venv venv
   source venv/Scripts/activate
   pip install -r requirements.txt
   ```
### 3. Run application

    ```bash
    python app.py
    ```pip list
