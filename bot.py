import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ========== ТОКЕН БОТА ==========
BOT_TOKEN = "8706929511:AAEi7L-HGoebmaP9GS1VvJZXs9Eigqd27rI"

# ========== ТВОЁ РАСПИСАНИЕ ==========
# ВНИМАНИЕ! Это пример. ТЫ ДОЛЖЕН ЗАМЕНИТЬ на свои пары!
# Цифры: 0=ПН, 1=ВТ, 2=СР, 3=ЧТ, 4=ПТ, 5=СБ, 6=ВС

SCHEDULE = {
    "even": {  # ЧЕТНАЯ НЕДЕЛЯ
        0: ["09:00-10:30 Математика (ауд. 101)", "11:00-12:30 Физика (ауд. 202)"],
        1: ["10:00-11:30 Программирование (лаб. 301)"],
        2: [],
        3: ["09:00-10:30 Английский (онлайн)"],
        4: ["13:00-14:30 Физкультура"],
        5: [],
        6: []
    },
    "odd": {  # НЕЧЕТНАЯ НЕДЕЛЯ
        0: ["09:00-10:30 Философия (ауд. 105)", "12:00-13:30 Дискретная математика (ауд. 110)"],
        1: ["11:00-12:30 Базы данных (лаб. 305)"],
        2: ["14:00-15:30 Web-разработка (ауд. 401)"],
        3: [],
        4: ["10:00-11:30 Экономика"],
        5: [],
        6: []
    }
}

def get_current_week_type():
    week_number = datetime.now().isocalendar()[1]
    if week_number % 2 == 0:
        return "even"
    else:
        return "odd"

def get_schedule_for_day(week_type, day_index):
    return SCHEDULE.get(week_type, {}).get(day_index, [])

def format_schedule(lessons):
    if not lessons:
        return "📭 Пар нет! Можно отдыхать 😊"
    text = "📚 *Твои пары:*\n"
    for i, lesson in enumerate(lessons, 1):
        text += f"{i}. {lesson}\n"
    return text

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📅 СЕГОДНЯ", callback_data="today"))
    builder.add(InlineKeyboardButton(text="⏩ ЗАВТРА", callback_data="tomorrow"))
    builder.add(InlineKeyboardButton(text="📆 КОНКРЕТНЫЙ ДЕНЬ", callback_data="pick_day"))
    builder.add(InlineKeyboardButton(text="🗓 ВСЯ НЕДЕЛЯ", callback_data="this_week"))
    builder.add(InlineKeyboardButton(text="🔄 2 НЕДЕЛИ", callback_data="two_weeks"))
    builder.adjust(1)
    return builder.as_markup()

def days_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ПН", callback_data="day_0"),
         InlineKeyboardButton(text="ВТ", callback_data="day_1"),
         InlineKeyboardButton(text="СР", callback_data="day_2")],
        [InlineKeyboardButton(text="ЧТ", callback_data="day_3"),
         InlineKeyboardButton(text="ПТ", callback_data="day_4"),
         InlineKeyboardButton(text="СБ", callback_data="day_5")],
        [InlineKeyboardButton(text="ВС", callback_data="day_6")],
        [InlineKeyboardButton(text="🔙 НАЗАД", callback_data="back_to_menu")]
    ])
    return kb

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    week_type = get_current_week_type()
    week_name = "ЧЕТНАЯ 📘" if week_type == "even" else "НЕЧЕТНАЯ 📙"
    await message.answer(
        f"🎓 *Привет, {message.from_user.first_name}!*\n\n"
        f"Я твой помощник по расписанию.\n"
        f"Сейчас *{week_name}* неделя.\n\n"
        f"Выбери, что хочешь узнать:",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    week_type = get_current_week_type()
    today_index = datetime.now().weekday()
    days_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    
    if callback.data == "today":
        lessons = get_schedule_for_day(week_type, today_index)
        week_name = "Четная" if week_type == "even" else "Нечетная"
        text = f"📅 *Сегодня ({days_ru[today_index]}, {week_name} неделя)*\n\n{format_schedule(lessons)}"
        await callback.message.answer(text, parse_mode="Markdown")
    
    elif callback.data == "tomorrow":
        tomorrow = datetime.now() + timedelta(days=1)
        day_idx = tomorrow.weekday()
        lessons = get_schedule_for_day