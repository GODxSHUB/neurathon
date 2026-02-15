import sqlite3
import json
from datetime import date, datetime

DB_NAME = "smart_companion.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # User Stats
    c.execute('''CREATE TABLE IF NOT EXISTS user_stats (
                    id INTEGER PRIMARY KEY,
                    points INTEGER DEFAULT 0,
                    completed_tasks INTEGER DEFAULT 0,
                    streak_days INTEGER DEFAULT 0,
                    last_active_date TEXT
                )''')
    # Current State
    c.execute('''CREATE TABLE IF NOT EXISTS current_state (
                    id INTEGER PRIMARY KEY,
                    mood TEXT,
                    task_input TEXT,
                    steps TEXT,
                    current_step_index INTEGER,
                    task_started BOOLEAN
                )''')
    # Daily Challenges
    c.execute('''CREATE TABLE IF NOT EXISTS daily_challenge (
                    date TEXT PRIMARY KEY,
                    challenge_text TEXT,
                    is_completed BOOLEAN
                )''')
    
    # Initialize defaults
    if c.execute("SELECT count(*) FROM user_stats").fetchone()[0] == 0:
        c.execute("INSERT INTO user_stats (id, points, completed_tasks, streak_days, last_active_date) VALUES (1, 0, 0, 0, ?)", (date.today(),))
    if c.execute("SELECT count(*) FROM current_state").fetchone()[0] == 0:
        c.execute("INSERT INTO current_state (id, mood, task_input, steps, current_step_index, task_started) VALUES (1, NULL, '', '[]', 0, 0)")
        
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    stats = c.execute("SELECT * FROM user_stats WHERE id=1").fetchone()
    state = c.execute("SELECT * FROM current_state WHERE id=1").fetchone()
    conn.close()
    
    return {
        "points": stats['points'],
        "completed_tasks": stats['completed_tasks'],
        "streak_days": stats['streak_days'],
        "mood": state['mood'],
        "task_input": state['task_input'],
        "steps": json.loads(state['steps']),
        "current_step": state['current_step_index'],
        "task_started": bool(state['task_started'])
    }

def update_stats(points, completed_tasks, streak_days):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE user_stats SET points=?, completed_tasks=?, streak_days=?, last_active_date=? WHERE id=1", 
              (points, completed_tasks, streak_days, date.today()))
    conn.commit()
    conn.close()

def save_current_state(mood, task_input, steps, current_step, task_started):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE current_state SET mood=?, task_input=?, steps=?, current_step_index=?, task_started=? WHERE id=1", 
              (mood, task_input, json.dumps(steps), current_step, int(task_started)))
    conn.commit()
    conn.close()

# --- NEW: JSON EXPORT FUNCTION ---
def export_tasks_to_json():
    """Reads current task data and returns a JSON string."""
    data = load_data()
    
    export_data = {
        "export_date": str(date.today()),
        "user_stats": {
            "total_points": data["points"],
            "tasks_completed": data["completed_tasks"],
            "current_streak": data["streak_days"]
        },
        "current_active_work": {
            "task_title": data["task_input"],
            "mood": data["mood"],
            "progress": f"{data['current_step']}/{len(data['steps'])}",
            "steps": data["steps"]
        }
    }
    return json.dumps(export_data, indent=4)