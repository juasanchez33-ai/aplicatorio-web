import sqlite3
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import webbrowser
import threading
import time
from datetime import datetime, timedelta
try:
    from routes import auth, movements, investments, debts_and_payments
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from routes import auth, movements, investments, debts_and_payments

# Data Persistence Setup (SQLite)
DB_FILE = "../database/finanzas_personales.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def open_browser():
    """Opens the browser after a short delay to ensure the server is up."""
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    yield

app = FastAPI(lifespan=lifespan)

# Register Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(movements.router, prefix="/api/movements", tags=["movements"])
app.include_router(investments.router, prefix="/api/investments", tags=["investments"])
app.include_router(debts_and_payments.router, prefix="/api", tags=["debts_and_payments"])

# Templates & Static Files
templates = Jinja2Templates(directory="../frontend")

# Mounting different directories for static assets as requested by the user structure
app.mount("/css", StaticFiles(directory="../frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")
app.mount("/assets", StaticFiles(directory="../frontend/assets"), name="assets")

# Main Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

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

@app.get("/categories", response_class=HTMLResponse)
async def categories_page(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})

@app.get("/debts", response_class=HTMLResponse)
async def debts_page(request: Request):
    return templates.TemplateResponse("debts.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
