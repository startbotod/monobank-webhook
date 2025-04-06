from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from db import activate_subscription, init_db  # Импортируем из db.py
import logging

app = FastAPI()

# Инициализация БД
init_db()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/monobank-webhook")
async def ping():
    return PlainTextResponse("OK", status_code=200)

@app.post("/monobank-webhook")
async def monobank_webhook(request: Request):
    try:
        data = await request.json()
        logger.info(f"Received webhook data: {data}")

        if "invoiceId" in data and "status" in data:
            status = data["status"]
            reference = data.get("reference", "")

            if status == "success" and reference.startswith("bot_sub_"):
                try:
                    user_id = int(reference.split("_")[-1])
                    activate_subscription(user_id)
                    logger.info(f"✅ Subscription activated for user_id {user_id}")
                except (ValueError, IndexError) as e:
                    logger.error(f"Error processing reference: {e}")

        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"ok": False, "error": str(e)}, 500