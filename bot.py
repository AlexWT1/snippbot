import os
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from database import async_session
from crud import create_snippet, get_snippet_by_name, get_snippets_by_user, delete_snippet_by_name

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
router = Router()

user_state = {}  # user_id -> {'action': 'add_name'|'add_content', 'name': ...}

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Используй:\n/add — добавить сниппет\n/get [название] — получить\n/list — список\n/delete [название] — удалить")

@router.message(Command("add"))
async def cmd_add(message: Message):
    user_id = message.from_user.id
    user_state[user_id] = {'action': 'add_name'}
    await message.answer("Введите название сниппета:")

@router.message(Command("list"))
async def cmd_list(message: Message):
    async with async_session() as db:
        snippets = await get_snippets_by_user(db, message.from_user.id)
    if not snippets:
        await message.answer("У вас нет сниппетов.")
        return
    names = "\n".join([f"• {s.name}" for s in snippets])
    await message.answer(f"Ваши сниппеты:\n{names}")

@router.message(Command("get"))
async def cmd_get(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Используй: /get название")
        return
    name = parts[1]
    async with async_session() as db:
        snippet = await get_snippet_by_name(db, message.from_user.id, name)
    if snippet:
        await message.answer(f"```\n{snippet.content}\n```", parse_mode="MarkdownV2")  # экранируем спецсимволы
    else:
        await message.answer("Сниппет не найден.")

@router.message(Command("delete"))
async def cmd_delete(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Используй: /delete название")
        return
    name = parts[1]
    async with async_session() as db:
        await delete_snippet_by_name(db, message.from_user.id, name)
    await message.answer(f"Сниппет '{name}' удалён.")

# Обработка текста (для ввода названия и содержимого)
@router.message()
async def handle_text(message: Message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in user_state:
        return  # не в процессе добавления

    state = user_state[user_id]

    if state['action'] == 'add_name':
        user_state[user_id] = {'action': 'add_content', 'name': text}
        await message.answer("Теперь введите содержимое сниппета (можно многострочно):")
    elif state['action'] == 'add_content':
        name = state['name']
        async with async_session() as db:
            await create_snippet(db, user_id, name, text)
        del user_state[user_id]
        await message.answer(f"Сниппет '{name}' сохранён!")