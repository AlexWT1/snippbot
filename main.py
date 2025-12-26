import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from bot import router, bot
from aiogram import Dispatcher

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Запускаем бота в режиме polling
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.create_task(dp.start_polling(bot))
    
    yield
    
    # Завершение
    await engine.dispose()
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "SnippBot is running!"}