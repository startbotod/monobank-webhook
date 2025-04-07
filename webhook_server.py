from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from db import activate_subscription
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.get("/monobank-webhook")
async def ping():
    return PlainTextResponse("OK")

@app.post("/monobank-webhook")
async def monobank_webhook(request: Request):
    data = await request.json()
    logging.info(f"Webhook: {data}")

    if data.get("status") == "success" and data.get("reference", "").startswith("bot_sub_"):
        try:
            user_id = int(data["reference"].split("_")[-1])
            activate_subscription(user_id)
            logging.info(f"✅ Активована підписка для user_id: {user_id}")
        except Exception as e:
            logging.error(f"❌ Error: {e}")

    return {"ok": True}