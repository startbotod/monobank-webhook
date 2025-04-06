from fastapi import FastAPI, Request
import sqlite3
from datetime import datetime, timedelta
from fastapi.responses import PlainTextResponse

app = FastAPI()  # Сначала создаём app

DB_PATH = "users.db"

@app.get("/monobank-webhook")
async def ping():
    return PlainTextResponse("OK", status_code=200)

@app.post("/monobank-webhook")
async def monobank_webhook(request: Request):
    data = await request.json()
    print("Got webhook:", data)

    if "invoiceId" in data and "status" in data:
        status = data["status"]
        reference = data.get("reference", "")

        if status == "success" and reference.startswith("bot_sub_"):
            user_id = int(reference.split("_")[-1])
            activate_subscription(user_id)
            print(f"✅ Подписка активирована для user_id {user_id}")

    return {"ok": True}

def activate_subscription(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    expires_at = datetime.now() + timedelta(days=90)
    c.execute('''
        UPDATE users SET subscription_expires_at = ? WHERE user_id = ?
    ''', (expires_at.strftime("%Y-%m-%d %H:%M:%S"), user_id))
    conn.commit()
    conn.close()
