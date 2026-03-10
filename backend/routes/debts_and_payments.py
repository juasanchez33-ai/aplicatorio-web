from fastapi import APIRouter, Request
from typing import Optional
import sqlite3

router = APIRouter()
DB_FILE = "../database/finanzas_personales.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/debts")
async def get_debts(email: Optional[str] = None):
    if not email:
        return {"status": "success", "data": []}
    conn = get_db_connection()
    debts = conn.execute('SELECT * FROM debts WHERE user_email = ? ORDER BY id DESC', (email,)).fetchall()
    conn.close()
    return {"status": "success", "data": [dict(d) for d in debts]}

@router.post("/add-debt")
async def add_debt(request: Request):
    data = await request.json()
    email = data.get("email")
    debt = data.get("debt") # {name, total_amount, paid_amount, due_date}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO debts (user_email, name, total_amount, paid_amount, due_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (email, debt["name"], debt["total_amount"], debt["paid_amount"], debt["due_date"]))
    conn.commit()
    conn.close()
    return {"status": "success"}

@router.get("/payments")
async def get_payments(email: Optional[str] = None):
    if not email:
        return {"status": "success", "data": []}
    conn = get_db_connection()
    payments = conn.execute('SELECT * FROM payments WHERE user_email = ? ORDER BY id DESC', (email,)).fetchall()
    conn.close()
    return {"status": "success", "data": [dict(p) for p in payments]}

@router.post("/add-payment")
async def add_payment(request: Request):
    data = await request.json()
    email = data.get("email")
    payment = data.get("payment") # {name, amount, due_date}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO payments (user_email, name, amount, due_date)
    VALUES (?, ?, ?, ?)
    ''', (email, payment["name"], payment["amount"], payment["due_date"]))
    conn.commit()
    conn.close()
    return {"status": "success"}
