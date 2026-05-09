import sqlite3, json, os
from datetime import datetime

DB = os.path.join(os.path.dirname(__file__), 'nexus.db')

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            data TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            messages TEXT NOT NULL DEFAULT '[]',
            started_at TEXT DEFAULT (datetime('now')),
            ended_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')
    conn.commit()
    conn.close()

def get_or_create_user(username):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
    if not user:
        conn.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
        conn.execute('INSERT INTO profiles (user_id, data) VALUES (?, ?)', (user['id'], json.dumps(default_profile())))
        conn.commit()
    conn.close()
    return dict(user)

def get_profile(user_id):
    conn = get_db()
    row = conn.execute('SELECT data FROM profiles WHERE user_id=?', (user_id,)).fetchone()
    conn.close()
    return json.loads(row['data']) if row else default_profile()

def save_profile(user_id, data):
    conn = get_db()
    conn.execute(
        'INSERT OR REPLACE INTO profiles (user_id, data, updated_at) VALUES (?,?,?)',
        (user_id, json.dumps(data), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_active_session(user_id):
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM sessions WHERE user_id=? AND ended_at IS NULL ORDER BY id DESC LIMIT 1',
        (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def create_session(user_id):
    conn = get_db()
    conn.execute('INSERT INTO sessions (user_id, messages) VALUES (?,?)', (user_id, '[]'))
    conn.commit()
    row = conn.execute('SELECT last_insert_rowid() as id').fetchone()
    session_id = row['id']
    conn.close()
    return session_id

def get_session_messages(session_id):
    conn = get_db()
    row = conn.execute('SELECT messages FROM sessions WHERE id=?', (session_id,)).fetchone()
    conn.close()
    return json.loads(row['messages']) if row else []

def append_message(session_id, role, content):
    messages = get_session_messages(session_id)
    messages.append({'role': role, 'content': content, 'ts': datetime.now().isoformat()})
    conn = get_db()
    conn.execute('UPDATE sessions SET messages=? WHERE id=?', (json.dumps(messages), session_id))
    conn.commit()
    conn.close()
    return messages

def end_session(session_id):
    conn = get_db()
    conn.execute('UPDATE sessions SET ended_at=? WHERE id=?', (datetime.now().isoformat(), session_id))
    conn.commit()
    conn.close()

def all_users():
    conn = get_db()
    rows = conn.execute('SELECT u.*, p.data as profile_data FROM users u LEFT JOIN profiles p ON u.id=p.user_id').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def default_profile():
    return {
        "name": "",
        "style": "unknown",           # casual / formal / technical / simple
        "pace": "medium",             # fast / medium / slow
        "depth": "medium",            # surface / medium / deep
        "analogies": [],              # cooking, sports, nature, tech...
        "fears": [],                  # things that make them hesitate
        "strengths": [],              # what they respond well to
        "topics": [],                 # domains they've asked about
        "key_moments": [],            # breakthroughs, aha-moments
        "session_count": 0,
        "total_messages": 0,
        "voice_user": False,
        "notes": ""
    }
