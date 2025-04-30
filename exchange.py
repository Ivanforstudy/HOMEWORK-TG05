import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, EXCHANGE_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот, который может показать курс валют и рассказать шутку.\n\nДоступные команды:\n/convert — конвертация валют\n/joke — случайная шутка")

@dp.message(Command("convert"))
async def convert(message: Message):
    try:
        base_currency = "USD"
        target_currency = "EUR"
        amount = 100

        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{base_currency}/{target_currency}/{amount}"
        response = requests.get(url)
        data = response.json()

        if data["result"] == "success":
            converted_amount = data["conversion_result"]
            await message.answer(f"{amount} {base_currency} = {converted_amount} {target_currency}")
        else:
            await message.answer("Не удалось получить данные о курсе валют.")
    except Exception as e:
        await message.answer("Произошла ошибка при получении данных.")

@dp.message(Command("joke"))
async def joke(message: Message):
    try:
        url = "https://v2.jokeapi.dev/joke/Any"
        response = requests.get(url)
        data = response.json()

        if data["type"] == "single":
            await message.answer(data["joke"])
        else:
            await message.answer(f"{data['setup']}\n{data['delivery']}")
    except Exception as e:
        await message.answer("Не удалось получить шутку.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
