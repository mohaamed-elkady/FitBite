import streamlit as st
import psycopg

# database connection

connection_str = st.secrets['connection_str']


# making the connection

def get_connection():
    return psycopg.connect(connection_str, sslmode="require")


# making the users table

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# creating a user

def create_user(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (username, xp, level, streak)
        VALUES (%s, 0, 1, 0)
        ON CONFLICT (username) DO NOTHING
    """, (username,))

    conn.commit()
    conn.close()


# loading user data

def load_user(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT xp, level, streak
        FROM users
        WHERE username = %s
    """, (username,))

    data = cur.fetchone()

    conn.close()
    return data


# saving user data

def save_user(username, xp, level, streak):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET xp = %s,
            level = %s,
            streak = %s
        WHERE username = %s
    """, (xp, level, streak, username))

    conn.commit()
    conn.close()


# leaderboard

def get_leaderboard():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, level, xp
        FROM users
        ORDER BY level DESC, xp DESC
        LIMIT 10
    """)

    data = cur.fetchall()

    conn.close()
    return data