from fastapi import APIRouter, HTTPException
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

router = APIRouter()

def get_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("BASE DE DATOS PERMAQR").sheet1
        return sheet
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/maquina/{id}")
def get_maquina(id: str):
    sheet = get_sheet()
    all_records = sheet.get_all_records()
    for record in all_records:
        if record["ID"].strip() == id.strip():
            return record
    raise HTTPException(status_code=404, detail="Máquina no encontrada")