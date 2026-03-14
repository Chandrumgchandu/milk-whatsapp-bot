from fastapi import FastAPI
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

from fastapi import Form
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

# Google Sheets connection
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "milk-bot-490207-7269767d1492.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("milk_database").sheet1


@app.get("/")
def home():
    return {"message": "Milk Bot Running"}


@app.get("/add")
def add_entry(phone: str, quantity: float):

    now = datetime.now()

    sheet.append_row([
        phone,
        quantity,
        now.date().isoformat(),
        now.strftime("%H:%M")
    ])

    return {"status": "entry stored"}

@app.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...)
):

    message = Body.strip()

    response = MessagingResponse()

    try:
        quantity = float(message)

        now = datetime.now()

        sheet.append_row([
            From,
            quantity,
            now.date().isoformat(),
            now.strftime("%H:%M")
        ])

        response.message(f"Milk recorded: {quantity} L")

    except:
        response.message("Send milk quantity like 3.5")

    return str(response)
