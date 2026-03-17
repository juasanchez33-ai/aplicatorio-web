import sqlite3
import os
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
import uvicorn
import webbrowser
import threading
import time
from datetime import datetime, timedelta
import json
import urllib.request
import urllib.parse
import random
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import StringIO
import csv

load_dotenv(override=True)

# Data Persistence Setup (SQLite)
DB_FILE = "aplicativo_web.db"

def send_email_otp(target_email, code):
    """
    Envía el código de seguridad por correo electrónico usando SMTP.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    print(f"DEBUG: Intentando enviar email a {target_email}...")
    
    if not all([smtp_user, smtp_pass]):
        print("ERROR: Credenciales SMTP (SMTP_USER/SMTP_PASS) no encontradas en .env")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = f"Seguridad Aplicativo Web <{smtp_user}>"
        msg['To'] = target_email
        msg['Subject'] = f"{code} es tu código de verificación"

        body = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #030712; color: #fff; padding: 40px;">
            <div style="max-width: 500px; margin: auto; background: #0f172a; padding: 40px; border-radius: 20px; border: 1px solid #1e293b; text-align: center;">
                <h1 style="color: #00f0ff; text-transform: uppercase; letter-spacing: 2px; font-size: 20px;">Verificación de Seguridad</h1>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 20px;">Has solicitado un código de acceso para tu cuenta en <strong>Aplicativo Web de Finanzas</strong>.</p>
                <div style="background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3); padding: 20px; border-radius: 15px; margin: 30px 0;">
                    <span style="font-size: 42px; font-weight: 900; letter-spacing: 8px; color: #00f0ff;">{code}</span>
                </div>
                <p style="color: #475569; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">Este código expirará en 10 minutos por tu seguridad.</p>
                <hr style="border: 0; border-top: 1px solid #1e293b; margin: 30px 0;">
                <p style="color: #334155; font-size: 10px;">Si no solicitaste este código, por favor ignora este mensaje o contacta a soporte.</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        print(f"DEBUG: Conectando a {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        print(f"DEBUG: Autenticando SMTP como {smtp_user}...")
        p_len = len(str(smtp_pass or '').strip())
        print(f"DEBUG: Longitud de SMTP_PASS: {p_len} caracteres.")
        if p_len > 0:
            p_val = str(smtp_pass or "").strip()
            print(f"DEBUG: Formato: {p_val[:2]}...{p_val[-2:]}")
        server.login(str(smtp_user or "").strip(), str(smtp_pass or "").strip())
        server.send_message(msg)
        server.quit()
        print(f"SUCCESS: Email enviado correctamente a {target_email}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("\n" + "="*60)
        print("ERROR DE AUTENTICACIÓN SMTP")
        print("Gmail requiere una 'Contraseña de Aplicación' (App Password).")
        print("1. Ve a: https://myaccount.google.com/apppasswords")
        print("2. Genera una contraseña para 'Correo' y 'Windows Computer'.")
        print("3. Copia el código de 16 letras en el campo SMTP_PASS de tu .env")
        print("="*60 + "\n")
        return False
    except Exception as e:
        print(f"ERROR CRÍTICO SMTP: {e}")
        return False

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def open_browser():
    # Wait a moment for the server to be fully ready
    time.sleep(3)
    url = "http://localhost:8000"
    try:
        # Try to find Google Chrome specifically
        chrome_path = None
        # Common paths for Chrome on Windows
        paths = [
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        ]
        for path in paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if chrome_path:
            # Register chrome and open
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get('chrome').open(url)
        else:
            # Fallback to default browser
            webbrowser.open(url)
    except Exception as e:
        print(f"Error opening browser: {e}")
        webbrowser.open(url)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Check SMTP and open browser
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    if not all([smtp_user, smtp_pass]):
        print("\n" + "#" * 60)
        print("  AVISO: Credenciales SMTP no detectadas en .env")
        print("  El sistema de seguridad usará la CONSOLA para los códigos.")
        print("  Configura SMTP_USER y SMTP_PASS para envíos reales.")
        print("#" * 60 + "\n")
    else:
        print(f"\nSISTEMA: SMTP configurado para {smtp_user}. Listo para enviar correos.\n")

    if os.getenv("RENDER") is None:
        threading.Thread(target=open_browser, daemon=True).start()
    yield
    # Shutdown logic if needed
    pass

app = FastAPI(lifespan=lifespan)

# Routes
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})



@app.get("/movements", response_class=HTMLResponse)
async def movements_page(request: Request):
    return templates.TemplateResponse("movements.html", {"request": request})

@app.get("/news", response_class=HTMLResponse)
async def news(request: Request):
    return templates.TemplateResponse("news.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Renderiza la página de registro de nuevos usuarios.
    """
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/recover-password", response_class=HTMLResponse)
async def recover_password(request: Request):
    return templates.TemplateResponse("recover-password.html", {"request": request})

@app.get("/confirmation", response_class=HTMLResponse)
async def confirmation(request: Request):
    """
    Renderiza la página de confirmación (ej. de registro o recuperación de contraseña).
    """
    return templates.TemplateResponse("confirmation.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/study", response_class=HTMLResponse)
async def study_page(request: Request):
    return templates.TemplateResponse("study.html", {"request": request})

@app.get("/payments", response_class=HTMLResponse)
async def payments_page(request: Request):
    return templates.TemplateResponse("payments.html", {"request": request})

@app.get("/investments", response_class=HTMLResponse)
async def investments_page(request: Request):
    return templates.TemplateResponse("investments.html", {"request": request})

@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio_page(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request})

@app.get("/categories", response_class=HTMLResponse)
async def categories_page(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})

@app.get("/debts", response_class=HTMLResponse)
async def debts_page(request: Request):
    return templates.TemplateResponse("debts.html", {"request": request})

@app.get("/api/export-expenses")
async def export_expenses(email: Optional[str] = None):
    conn = get_db_connection()
    if email:
        movements = conn.execute('SELECT date, concept, amount, category FROM movements WHERE user_email = ? AND type = "expense"', (email,)).fetchall()
    else:
        # Fallback to simulated data if no email
        movements = [
            {"date": "2026-02-25", "concept": "Suscripcion Prime", "amount": 14.99, "category": "Ocio"},
            {"date": "2026-02-24", "concept": "Mercado Semanal", "amount": 85.20, "category": "Alimentacion"}
        ]
    conn.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Fecha", "Concepto", "Monto", "Categoria"])
    for m in movements:
        writer.writerow([m["date"], m["concept"], m["amount"], m["category"]])
    
    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=gastos_Aplicativo Web para el Manejo de Finanzas Personales.csv"}
    )

@app.get("/api/movements")
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
 
@app.get("/api/profile")
async def get_profile(email: str):
    conn = get_db_connection()
    profile = conn.execute('SELECT * FROM user_profiles WHERE user_email = ?', (email,)).fetchone()
    settings = conn.execute('SELECT * FROM user_settings WHERE user_email = ?', (email,)).fetchone()
    conn.close()
    
    return {
        "status": "success",
        "data": {
            "phone_number": profile["phone_number"] if profile else "",
            "two_factor_enabled": (settings["two_factor_enabled"] == 1) if settings else False
        }
    }

# reCAPTCHA logic removed (replaced by custom internal security)

@app.post("/api/profile")
async def update_profile(request: Request):
    data = await request.json()
    email = data.get("email")
    phone = data.get("phone")
    mfa_enabled = data.get("two_factor_enabled")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update profile (phone)
    if phone is not None:
        cursor.execute('''
        INSERT INTO user_profiles (user_email, first_name, phone_number, joined_at)
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(user_email) DO UPDATE SET phone_number = excluded.phone_number
        ''', (email, email.split('@')[0], phone))
        
    # Update settings (MFA)
    if mfa_enabled is not None:
        mfa_val = 1 if mfa_enabled else 0
        cursor.execute('''
        INSERT INTO user_settings (user_email, two_factor_enabled)
        VALUES (?, ?)
        ON CONFLICT(user_email) DO UPDATE SET two_factor_enabled = excluded.two_factor_enabled
        ''', (email, mfa_val))
        
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/api/add-movement")
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

@app.get("/api/market-data")
async def get_market_data():
    # Mock data for demonstration
    return {
        "status": "success",
        "data": {
            "btc": {"price": 44120.50, "change": 2.45},
            "eth": {"price": 2450.12, "change": 1.20},
            "spx": {"price": 4890.97, "change": 0.85},
            "aapl": {"price": 189.43, "change": -1.12}
        }
    }



@app.get("/api/debts")
async def get_debts(email: Optional[str] = None):
    if not email:
        return {"status": "success", "data": []}
    conn = get_db_connection()
    debts = conn.execute('SELECT * FROM debts WHERE user_email = ? ORDER BY id DESC', (email,)).fetchall()
    conn.close()
    return {"status": "success", "data": [dict(d) for d in debts]}

@app.post("/api/add-debt")
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

@app.get("/api/payments")
async def get_payments(email: Optional[str] = None):
    if not email:
        return {"status": "success", "data": []}
    conn = get_db_connection()
    payments = conn.execute('SELECT * FROM payments WHERE user_email = ? ORDER BY id DESC', (email,)).fetchall()
    conn.close()
    return {"status": "success", "data": [dict(p) for p in payments]}

@app.post("/api/add-payment")
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

@app.post("/api/security/send-otp")
async def send_security_otp(request: Request):
    """
    Sistema de seguridad personalizado: Genera y envía un código de 6 dígitos.
    """
    try:
        data = await request.json()
        email = data.get("email")
        if not email:
            return JSONResponse(content={"status": "error", "message": "Email requerido"}, status_code=400)

        otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
        expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        # Aseguramos que la tabla exista
        cursor.execute('CREATE TABLE IF NOT EXISTS security_codes (email TEXT PRIMARY KEY, code TEXT, expires_at TEXT)')
        cursor.execute('INSERT OR REPLACE INTO security_codes (email, code, expires_at) VALUES (?, ?, ?)', (email, otp, expires_at))
        conn.commit()
        conn.close()
        
        # Envío real por Email
        email_sent = send_email_otp(email, otp)
        
        # Mostrar en consola si el modo DEBUG está activo o si el envío falló
        show_in_console = os.getenv("DEBUG_SHOW_OTP_IN_CONSOLE", "True").lower() == "true"
        if show_in_console or not email_sent:
            print("\n" + "!" * 50)
            print(f"  SISTEMA DE SEGURIDAD - APLICATIVO WEB")
            print(f"  CÓDIGO DE VERIFICACIÓN PARA: {email}")
            print(f"  TU CÓDIGO ES: {otp}")
            print(f"  ESTADO DEL ENVÍO EMAIL: {'EXITOSO' if email_sent else 'FALLIDO'}")
            print("!" * 50 + "\n")
        
        if email_sent:
            return {"status": "success", "message": "Código de seguridad enviado a tu correo."}
        else:
            return {"status": "success", "message": "No se pudo enviar el correo. Revisa la consola del servidor para ver el código y verificar tus credenciales SMTP."}
            
    except Exception as e:
        print(f"Error en send_security_otp: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/api/security/verify-otp")
async def verify_security_otp(request: Request):
    """
    Valida el código de seguridad ingresado por el usuario.
    """
    try:
        data = await request.json()
        email = data.get("email")
        code = data.get("code")
        
        if not email or not code:
            return JSONResponse(content={"status": "error", "message": "Faltan datos"}, status_code=400)

        conn = get_db_connection()
        record = conn.execute('SELECT * FROM security_codes WHERE email = ? AND code = ?', (email, code)).fetchone()
        conn.close()
        
        if record:
            expires_at = datetime.fromisoformat(record["expires_at"])
            if datetime.now() < expires_at:
                return {"status": "success"}
            else:
                return {"status": "error", "message": "El código ha expirado. Solicita uno nuevo."}
        
        return {"status": "error", "message": "El código ingresado es incorrecto."}
    except Exception as e:
        print(f"Error en verify_security_otp: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=(os.getenv("RENDER") is None))
