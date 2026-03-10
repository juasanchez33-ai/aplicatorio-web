from fastapi import APIRouter, Request
from typing import Optional
import sqlite3
from datetime import datetime, timedelta

router = APIRouter()
DB_FILE = "../database/finanzas_personales.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
async def get_movements(email: Optional[str] = None, category: Optional[str] = None, date_range: Optional[str] = None):
    if not email:
        return {"status": "success", "data": []}
    
    conn = get_db_connection()
    query = 'SELECT * FROM movements WHERE user_email = ?'
    params = [email]

    if category and category != 'All':
        query += ' AND category = ?'
        params.append(category)

    if date_range == '24h':
        limit_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        query += ' AND date >= ?'
        params.append(limit_date)
    elif date_range == '7d':
        limit_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        query += ' AND date >= ?'
        params.append(limit_date)
    elif date_range == '30d':
        limit_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        query += ' AND date >= ?'
        params.append(limit_date)

    query += ' ORDER BY date DESC, id DESC'
    movements = conn.execute(query, params).fetchall()
    conn.close()
    
    return {"status": "success", "data": [dict(m) for m in movements]}

@router.post("/add")
async def add_movement(request: Request):
    data = await request.json()
    email = data.get("email")
    movement = data.get("movement") # {type, concept, amount, date, category}
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO movements (user_email, type, concept, amount, date, category)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (email, movement["type"], movement["concept"], movement["amount"], movement["date"], movement["category"]))
    
    conn.commit()
    conn.close()
    return {"status": "success"}
