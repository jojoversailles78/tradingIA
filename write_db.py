content = '''import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    if not DATABASE_URL:
        return False
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS agents_state (
                id VARCHAR(50) PRIMARY KEY,
                data JSONB NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("DB init error:", e)
        return False

def load_agents_db():
    if not DATABASE_URL:
        return None
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, data FROM agents_state")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if not rows:
            return None
        return {row["id"]: row["data"] for row in rows}
    except Exception as e:
        print("DB load error:", e)
        return None

def save_agents_db(state):
    if not DATABASE_URL:
        return False
    try:
        conn = get_conn()
        cur = conn.cursor()
        for agent_id, data in state.items():
            cur.execute("""
                INSERT INTO agents_state (id, data, updated_at)
                VALUES (%s, %s, NOW())
                ON CONFLICT (id) DO UPDATE
                SET data = EXCLUDED.data, updated_at = NOW()
            """, (agent_id, json.dumps(data, default=str)))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("DB save error:", e)
        return False

def save_single_agent_db(agent_id, data):
    if not DATABASE_URL:
        return False
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO agents_state (id, data, updated_at)
            VALUES (%s, %s, NOW())
            ON CONFLICT (id) DO UPDATE
            SET data = EXCLUDED.data, updated_at = NOW()
        """, (agent_id, json.dumps(data, default=str)))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("DB save single error:", e)
        return False
'''

with open('backend/app/db.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK - db.py cree')