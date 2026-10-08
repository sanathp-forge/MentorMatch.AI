"""
Database management module for MentorMatch AI using SQLite.
Handles table creation, queries, insertions, and updates.
"""

import sqlite3
import os
import pandas as pd
from typing import Optional, List, Dict, Any

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "mentormatch.db")

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str = DB_PATH) -> None:
    """Initialize all SQLite tables for MentorMatch AI."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        department TEXT,
        semester INTEGER,
        cgpa REAL,
        skills TEXT,
        interests TEXT,
        career_goal TEXT,
        target_role TEXT,
        experience_level TEXT,
        projects TEXT,
        preferred_learning_style TEXT,
        communication_preference TEXT,
        availability TEXT,
        career_readiness_score INTEGER,
        resume_score INTEGER,
        confidence_score INTEGER,
        location TEXT,
        bio TEXT
    );

    CREATE TABLE IF NOT EXISTS mentors (
        mentor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        company TEXT,
        industry TEXT,
        department TEXT,
        experience_years INTEGER,
        skills TEXT,
        specializations TEXT,
        mentoring_style TEXT,
        availability TEXT,
        communication_preference TEXT,
        rating REAL,
        sessions_completed INTEGER,
        success_rate INTEGER,
        bio TEXT
    );

    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        student_id TEXT,
        mentor_id TEXT,
        date TEXT,
        topic TEXT,
        duration INTEGER,
        status TEXT,
        rating REAL,
        student_feedback TEXT,
        mentor_feedback TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (mentor_id) REFERENCES mentors(mentor_id)
    );

    CREATE TABLE IF NOT EXISTS feedback (
        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        mentor_id TEXT,
        rating REAL,
        feedback TEXT,
        skills_improved TEXT,
        confidence_before INTEGER,
        confidence_after INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS mentor_requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        mentor_id TEXT,
        status TEXT DEFAULT 'Pending',
        message TEXT,
        target_role TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        title TEXT,
        message TEXT,
        category TEXT,
        is_read INTEGER DEFAULT 0,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        target_role TEXT,
        phase_number INTEGER,
        phase_name TEXT,
        skills TEXT,
        duration_weeks INTEGER,
        completion_pct INTEGER,
        recommended_resources TEXT,
        mentor_discussion_topic TEXT,
        capstone_project TEXT
    );

    CREATE TABLE IF NOT EXISTS skills (
        skill_name TEXT PRIMARY KEY,
        category TEXT,
        demand_level TEXT,
        trending_score INTEGER
    );
    """)

    conn.commit()
    conn.close()

def save_dataframe_to_table(df: pd.DataFrame, table_name: str, db_path: str = DB_PATH, if_exists: str = "replace") -> None:
    conn = get_connection(db_path)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    conn.close()

def load_table_as_df(table_name: str, db_path: str = DB_PATH) -> pd.DataFrame:
    conn = get_connection(db_path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

def insert_session(session_dict: Dict[str, Any], db_path: str = DB_PATH) -> bool:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (session_id, student_id, mentor_id, date, topic, duration, status, rating, student_feedback, mentor_feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_dict.get("session_id"),
        session_dict.get("student_id"),
        session_dict.get("mentor_id"),
        session_dict.get("date"),
        session_dict.get("topic"),
        session_dict.get("duration", 45),
        session_dict.get("status", "Scheduled"),
        session_dict.get("rating", 0.0),
        session_dict.get("student_feedback", ""),
        session_dict.get("mentor_feedback", "")
    ))
    conn.commit()
    conn.close()
    return True

def insert_feedback(feedback_dict: Dict[str, Any], db_path: str = DB_PATH) -> bool:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (student_id, mentor_id, rating, feedback, skills_improved, confidence_before, confidence_after)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        feedback_dict.get("student_id"),
        feedback_dict.get("mentor_id"),
        feedback_dict.get("rating"),
        feedback_dict.get("feedback"),
        feedback_dict.get("skills_improved"),
        feedback_dict.get("confidence_before"),
        feedback_dict.get("confidence_after")
    ))
    conn.commit()
    conn.close()
    return True

def insert_mentor_request(req_dict: Dict[str, Any], db_path: str = DB_PATH) -> bool:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mentor_requests (student_id, mentor_id, status, message, target_role)
        VALUES (?, ?, ?, ?, ?)
    """, (
        req_dict.get("student_id"),
        req_dict.get("mentor_id"),
        req_dict.get("status", "Pending"),
        req_dict.get("message"),
        req_dict.get("target_role")
    ))
    conn.commit()
    conn.close()
    return True

def get_notifications(student_id: str = "STU001", db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications WHERE student_id = ? OR student_id = 'ALL' ORDER BY id DESC", (student_id,))
    rows = cursor.fetchall()
    res = [dict(row) for row in rows]
    conn.close()
    return res

def add_notification(student_id: str, title: str, message: str, category: str = "Info", db_path: str = DB_PATH) -> None:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (student_id, title, message, category, is_read)
        VALUES (?, ?, ?, ?, 0)
    """, (student_id, title, message, category))
    conn.commit()
    conn.close()
