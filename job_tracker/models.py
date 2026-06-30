import sqlite3

DB_PATH = "applications.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company_name TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'applied',
            applied_date DATE,
            notes TEXT,
            job_link TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

def create_user(username, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    """, (username, email, password_hash))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_application(user_id, company_name, role, status, applied_date, notes, job_link):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (user_id, company_name, role, status, applied_date, notes, job_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, company_name, role, status, applied_date, notes, job_link))
    conn.commit()
    conn.close()

def get_applications(user_id, status_filter="all"):
    conn = get_connection()
    cursor = conn.cursor()

    if status_filter == "all":
        cursor.execute("""
            SELECT * FROM applications 
            WHERE user_id = ? 
            ORDER BY applied_date DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT * FROM applications 
            WHERE user_id = ? AND status = ?
            ORDER BY applied_date DESC
        """, (user_id, status_filter))

    applications = cursor.fetchall()
    conn.close()
    return applications

def get_application_by_id(app_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    application = cursor.fetchone()
    conn.close()
    return application

def update_application(app_id, company_name, role, status, applied_date, notes, job_link):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE applications 
        SET company_name=?, role=?, status=?, applied_date=?, notes=?, job_link=?
        WHERE id=?
    """, (company_name, role, status, applied_date, notes, job_link, app_id))
    conn.commit()
    conn.close()

def delete_application(app_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()

def get_stats(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM applications
        WHERE user_id = ?
        GROUP BY status
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    stats = {"applied": 0, "interview": 0, "rejected": 0, "offer": 0}
    for row in rows:
        stats[row["status"]] = row["count"]

    stats["total"] = sum(stats.values())
    return stats
