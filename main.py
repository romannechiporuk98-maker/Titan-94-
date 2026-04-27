import os
import asyncio
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle(msg: types.Message):
    await msg.answer("🚀 Titan 94 ACTIVE")

app = FastAPI()

@app.get("/")
def root():
    return {"status": "TITAN LIVE"}

@app.post("/scan")
def scan(data: dict):
    risk = 0
    flags = []

    if data.get("can_sell") is False:
        risk += 50
        flags.append("sell_blocked")

    if data.get("liquidity", 0) < 5000:
        risk += 30
        flags.append("low_liquidity")

    return {
        "risk": min(risk, 100),
        "flags": flags
    }

async def start():
    asyncio.create_task(dp.start_polling(bot))
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(start())
