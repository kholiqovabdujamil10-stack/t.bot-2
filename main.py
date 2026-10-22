from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio
from connection import *
from service import *
import os


load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_bot(message: Message):
    if await get_user_by_id(message.from_user.id):
        await message.answer(f"Hello @{message.from_user.username} how are you ?")
        await message.answer(f"Mr @{message.from_user.username} for seeing all comands enter /help")
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"Hello @{message.from_user.username}")

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(
    "📋 Task Manager — Help\n\n"
    "Welcome! Here are the available commands:\n\n"
    "🚀 /start — Start the bot\n"
    "❓ /help — Show this help message\n"
    "➕ /add_task — Create a new task\n"
    "📝 /get_my_tasks — View your tasks\n"
    "👤 /info — View your profile information\n"
    "🆔 /id — Get your Telegram ID\n"
    "👥 /get_all_user — View all registered users\n\n"
    "💡 Stay organized and get more done!"
)

@dp.message(Command("get_all_user"))
async def help(message: Message):
    users = await get_users()
    text = ""
    for user in users:
        text += f"""
            UserName: {user["username"]}
FullName: {user["full_name"]}
                """
    await message.answer(text)


@dp.message(Command("add_task"))
async def add_task(message: Message, command: CommandObject):
    data = command.args
    data = data.split("/")
    if await create_task(data[0], data[1], data[2], message.from_user.id):
        await message.answer(f"Task with name {data[0]} created successful ✅")
    else:
        await message.answer(f"Task with name {data[0]} get error in created")




@dp.message(Command("get_my_tasks"))
async def help(message: Message):
    tasks = await get_task_by_id(message.from_user.id)
    text = ""
    for task in tasks:
        text+= f"""
Id: {task['task_id']}  
Title: {task['title']}  
Caption: {task['caption']}
Dueration date: {task['due_date']}
Status: {task['status']}

Created at: {task['created_at']}


                             """
    await message.answer(text)


@dp.message(Command("info"))
async def info(message: Message):
    user = await get_user_by_id(message.from_user.id)
    if user:
        await message.answer(
            f"Username: @{user['username'] or 'None'}\n"
            f"Full name: {user['full_name']}\n"
            f"Telegram ID: {user['telegram_id']}"
        )
    else:
        await message.answer("User not found. Send /start first.")


@dp.message(Command("id"))
async def get_id(message: Message):
    await message.answer(
        f"Your Telegram ID: {message.from_user.id}"
    )
    


async def main():
    await create_table()
    print("Bot started")
    await dp.start_polling(bot)

    
if __name__ == "__main__":
    asyncio.run(main())