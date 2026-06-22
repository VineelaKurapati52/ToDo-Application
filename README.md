#Application Demo video#
https://drive.google.com/file/d/1AYhf8q8ANpYmDe4BiyLDg-kKRagsIBqC/view?usp=drivesdk


# PriorityFlow - Tasks & Focus Timer

PriorityFlow is a high-performance, web-based task management dashboard and productivity suite built using **Flask (Python)**, **SQLite3**, **HTML5**, **Bootstrap 5**, and **Lucide Icons**. 

It combines task tracking (with scheduling and priority badges) and focus aids (a Pomodoro timer and Stopwatch) in a unified, glassy user interface that supports persistent Light and Dark themes.

---

## Features

- **Task Management (CRUD)**: Create, read, update, and delete tasks dynamically.
- **Priority Classifications**: Visual indicators and badges for High (red), Medium (yellow), and Low (cyan) priority levels.
- **Due Date Scheduling**: Attach dates to tasks to visualize deadlines.
- **Task Analytics Metrics**: Real-time stats counting total tasks, pending count, completed count, and completion progress percentages.
- **Dynamic Task Toggling**: Check circle buttons to mark tasks completed or active.
- **Multi-Mode Focus Timer Widget**:
  * **Pomodoro Mode**: 25-minute timer with preset buttons for **Focus (25m)**, **Short Break (5m)**, and **Long Break (15m)**. Synthesized audio alarms trigger when time finishes.
  * **Stopwatch Mode**: A count-up timer ("Infinite Time") to log work sessions.
- **Glassmorphism Design**: Frosted glass panels with a thin golden shine border.
- **Light & Dark Theme Switcher**: Automatically saves your color preferences in `localStorage` for future visits.

---

## Folder Structure

```text
Todo-app/
│
├── templates/              # HTML Templates (Jinja2)
│   └── index.html          # Dynamic, responsive glassmorphic dashboard UI
│
├── app.py                  # Flask backend (Routes, DB Schema, and SQLite queries)
├── TODO.db                 # Local SQLite database file (auto-generated)
└── README.md               # Project documentation & run commands
```

---

## Prerequisites

Make sure you have Python installed on your system. You will need to install the `flask` library.

### Installing Dependencies

Open your command prompt or terminal and run:

```bash
pip install flask
```

---

## How to Run the Application

1. **Open your terminal** and navigate to the project directory:
   ```bash
   cd Todo-app
   ```

2. **Run the Flask application**:
   ```bash
   python app.py
   ```
   *(Note: Use `python3` or `py` if your environment uses alternative path mappings.)*

3. **Navigate to the web page**:
   Open your browser and type:
   ```
   http://127.0.0.1:5000/
   ```
