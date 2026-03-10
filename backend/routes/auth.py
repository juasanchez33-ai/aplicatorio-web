from fastapi import APIRouter, Request
import sqlite3

router = APIRouter()
DB_FILE = "../database/finanzas_personales.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@router.post("/register")
async def api_register(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    user = cursor.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if user:
        conn.close()
        return {"status": "error", "message": "Email already in use"}
    
    # Register user
    cursor.execute('''
    INSERT INTO users (email, password, name, is_new)
    VALUES (?, ?, ?, ?)
    ''', (email, password, f"{first_name} {last_name}", 1))
    
    conn.commit()
    conn.close()
    return {"status": "success", "user": {"email": email, "name": f"{first_name} {last_name}", "is_new": True}}

@router.post("/login")
async def api_login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
    conn.close()

    if user:
        return {"status": "success", "user": {"email": user["email"], "name": user["name"], "is_new": bool(user["is_new"])}}
    
    return {"status": "error", "message": "Invalid email or password"}
