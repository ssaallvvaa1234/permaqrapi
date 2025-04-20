from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Autenticación con Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

sheet = client.open("BASE DE DATOS PERMAQR").sheet1  # nombre exacto de la planilla

@app.get("/buscar")
def buscar(id: str):
    data = sheet.get_all_records()
    for row in data:
        if row.get("ID (QR)") == id:
            return list(row.values())
    return {"error": "No encontrado"}