from fastapi import APIRouter, Request
from typing import Optional
import sqlite3

router = APIRouter()
DB_FILE = "../database/finanzas_personales.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
async def get_investments(email: Optional[str] = None):
    if not email:
        return {"status": "success", "data": [], "performance": [0,0,0,0,0,0,0]}
    
    conn = get_db_connection()
    investments = conn.execute('SELECT * FROM investments WHERE user_email = ? ORDER BY id DESC', (email,)).fetchall()
    conn.close()
    
    # Calculate performance trend (mocked for now)
    performance = [20, 45, 28, 80, 77, 95, 110]
    
    return {
        "status": "success",
        "data": [dict(i) for i in investments],
        "performance": performance
    }

@router.post("/add")
async def add_investment(request: Request):
    data = await request.json()
    email = data.get("email")
    investment = data.get("investment") # {symbol, name, investment, current, pnl, type}
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO investments (user_email, symbol, name, investment, current, pnl, type)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (email, investment["symbol"], investment["name"], investment["investment"], investment["current"], investment["pnl"], investment["type"]))
    
    conn.commit()
    conn.close()
    return {"status": "success"}
