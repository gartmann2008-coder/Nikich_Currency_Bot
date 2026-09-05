import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(uvloop=False)

def get_currency_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💵 USD"),
                KeyboardButton(text="💶 EUR"),
            ],
            [
                KeyboardButton(text="💷 GBP"),
                KeyboardButton(text="💴 CNY"),
            ],
            [
                KeyboardButton(text="📊 Все курсы"),
                KeyboardButton(text="🔄 Обновить"),
            ]
        ],
        resize_keyboard=True,  
        one_time_keyboard=False 
    )
    return keyboard


def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    data = response.json()

    if data.get("result") != "success":
        return None

    return data["conversion_rate"]


@dp.message(Command("start"))
async def start_command(message: types.Message):
    keboard = get_currency_keyboard()
    await message.answer(
         "💵 Привет! Я покажу тебе курс валют.\n\n"
        "Выбери валюту на клавиатуре ниже:",
        reply_markup=keboard
        )


@dp.message()
async def handle_currency_text(message: types.Message):
    text = message.text.strip()

    if text == "💵 USD":
        rate = get_exchange_rate("USD", "RUB")
        answer = f"💵 1 USD = {rate:.2f} RUB" if rate else "❌ Не удалось получить курс USD"

    elif text == "💶 EUR":
        rate = get_exchange_rate("EUR", "RUB")
        answer = f"💶 1 EUR = {rate:.2f} RUB" if rate else "❌ Не удалось получить курс EUR"

    elif text == "💷 GBP":
            rate = get_exchange_rate("GBP", "RUB")
            answer = f"💷 1 GBP = {rate:.2f} RUB" if rate else "❌ Не удалось получить курс GBP"

    elif text == "💴 CNY":
            rate = get_exchange_rate("CNY", "RUB")
            answer = f"💴 1 CNY = {rate:.2f} RUB" if rate else "❌ Не удалось получить курс CNY"

    elif text == "📊 Все курсы":
        usd = get_exchange_rate("USD", "RUB")
        eur = get_exchange_rate("EUR", "RUB")
        gbp = get_exchange_rate("GBP", "RUB")
        cny = get_exchange_rate("CNY", "RUB")

        if usd and eur and gbp and cny:
            answer = (
                f"📊 **Курсы валют к рублю:**\n\n"
                f"💵 USD: {usd:.2f} ₽\n"
                f"💶 EUR: {eur:.2f} ₽\n"
                f"💷 GBP: {gbp:.2f} ₽\n"
                f"💴 CNY: {cny:.2f} ₽"
            )

        else:
            answer = "❌ Не удалось получить курсы. Попробуй позже."

    elif text == "🔄 Обновить":
        await message.answer("🔄 Курсы обновлены! Нажми на любую кнопку, чтобы увидеть актуальные данные.")
        return
    else:
        await  message.answer("❌ Неизвестная команда. Используй кнопки на клавиатуре.")
        return

    await message.answer(answer, parse_mode="Markdown")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
