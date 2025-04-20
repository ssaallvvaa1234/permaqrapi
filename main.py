import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# Middleware para permitir acceso desde cualquier origen (para tu app Flutter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Configuración desde variable de entorno
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
client = gspread.authorize(credentials)

# 🗂️ Asegurate que el nombre coincida con tu planilla
sheet = client.open("BASE DE DATOS PERMAQR").sheet1

@app.get("/")
def home():
    return {"message": "API PermaQR funcionando"}

@app.get("/buscar")
def buscar(id: str):
    try:
        data = sheet.get_all_records()
        for row in data:
            if row.get("ID (QR)") == id:
                return row
        return {"error": "ID no encontrado"}
    except Exception as e:
        return {"error": str(e)}