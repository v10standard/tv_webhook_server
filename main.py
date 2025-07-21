from fastapi import FastAPI, Request
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

app = FastAPI()

# Google Sheets setup
SERVICE_ACCOUNT_FILE = 'trap-wizard-cloud-logger-key.json'  # Make sure this matches your downloaded file name
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"  # Replace with your actual Google Sheet ID
SHEET_NAME = "Raw_Data"  # Name of the tab to write to

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

@app.post("/tv-webhook")
async def receive_tv_alert(request: Request):
    payload = await request.json()

    symbol = payload.get("symbol", "N/A")
    tf = payload.get("tf", "N/A")
    time = payload.get("time", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    rsi = payload.get("RSI", "")
    macd = payload.get("MACD", "")
    macd_signal = payload.get("MACD_Signal", "")
    wt1 = payload.get("WT1", "")
    wt2 = payload.get("WT2", "")

    row = [time, symbol, tf, rsi, macd, macd_signal, wt1, wt2]
    sheet.append_row(row)

    return {"status": "✅ Data logged to Google Sheets"}
