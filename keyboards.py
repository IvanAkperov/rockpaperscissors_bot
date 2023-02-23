from aiogram.types import ReplyKeyboardMarkup


ikb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
ikb1.add("🪨 Камень 🪨", "✂️Ножницы ✂️", "📄 Бумага 📄", "Отмена")
new_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
new_kb.add("играем", "не хочу").add("статистика игр")