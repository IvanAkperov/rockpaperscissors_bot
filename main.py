import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from keyboards import ikb1, new_kb


bot: Bot = Bot(token="API TOKEN")  # ваш токен бота, полученный у @BotFather
dp: Dispatcher = Dispatcher(bot)


USERS: dict = {}  # словарь пользователей, своего рода "база данных"
HELP: str = """Все очень просто. Мы оба делаем свой выбор - камень, ножницы или бумага.\n"
"Камень побеждает ножницы, бумага камень, а ножницы бумагу! Вы так же можете посмотреть статистику игр"""


async def on_startup(_):
    print("Бот запустился и готов к работе!")  # уведомление о готовности бота к работе


@dp.message_handler(commands=["start"])  # хэндлер на команду /start
async def process_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.username}! Давай сыграем с тобой в камень-ножницы бумага?\n"
                         f"Если возникли вопросы - пиши /help", reply_markup=new_kb)
    if message.from_user.id not in USERS:  # если id пользователя не в словаре
        USERS[message.from_user.id] = {    # то создаём под каждого пользователя свои данные
                            "user_wins": 0,  # победы пользователя
                            "games": 0,  # общее кол-во сыгранных партий
                            "bot_wins": 0,  # победы бота
                            "tie": 0,  # ничьи
                            "in_game": False  # статус игрока
}


@dp.message_handler(commands=["help"])  # хэндлер на команду /help
async def process_help(message: types.Message):
    await message.answer(HELP)


@dp.message_handler(lambda text: text.text.lower() in ("да", "давай", "давайте", "можно", "согласен", "погнали", "играем"))
async def process_beginning(message: types.Message):
    """
    Ф-ция, реагирующая на согласие пользователя начать игру
    """
    if not USERS[message.from_user.id]["in_game"]:  # если пользователь не в игре
        USERS[message.from_user.id]["in_game"] = True  # меняем его статус на состояние "в игре"
        await message.answer(f"Отлично! Делайте свой выбор!", reply_markup=ikb1)
    else:
        await message.answer("Так камень, ножницы или бумага?", reply_markup=ikb1)


@dp.message_handler(Text(equals="статистика игр"))
async def process_stat(message: types.Message):
    """
    Ф-ция, уведомляющая пользователя об общей статистике игр
    """
    await message.answer(f"СТАТИСТИКА ИГР:\n1. Всего игр сыграно: {USERS[message.from_user.id]['games']}"
                         f"\n2. Твои победы: {USERS[message.from_user.id]['user_wins']}"
                         f"\n3. Победы бота: {USERS[message.from_user.id]['bot_wins']}"
                         f"\n4. Ничьих: {USERS[message.from_user.id]['tie']}")


@dp.message_handler(Text(equals="Отмена"))
async def process_stat(message: types.Message):
    """
    Ф-ция, выключающая игру
    """
    if USERS[message.from_user.id]["in_game"]:  # если пользователь в игре
        USERS[message.from_user.id]["in_game"] = False  # меняем его статус на "вне игры"
        await message.answer("Жаль, буду ждать следующей игры!", reply_markup=new_kb)
    else:
        await message.answer("А что отменять то? Мы же не играем. "
                             "Кстати, могли бы поиграть, что скажете?", reply_markup=new_kb)


@dp.message_handler(lambda y: y.text.lower() in ("нет", "не", "не хочу", "отказываюсь", "не надо", "неа"))
async def process_no(message: types.Message):
    """
    Ф-ция, реагирующая на отказ пользователя от дальнейшей игры
    """
    if not USERS[message.from_user.id]["in_game"]:
        await message.answer("Очень жаль! Ничего, буду ждать вашего прихода!")
    else:
        await message.answer("Мы же сейчас с вами играем, делайте свой выбор!")


@dp.message_handler(lambda x: x.text in ("🪨 Камень 🪨", "✂️Ножницы ✂️", "📄 Бумага 📄"))
async def process_game(message: types.Message):
    """
    Ф-ция, обрабатывающая выбор пользователя. В дальнейшем делает случайный выбор для бота и сравнивает результаты.
    """
    if USERS[message.from_user.id]["in_game"]:
        USERS[message.from_user.id]["games"] += 1
        bot_choice = random.choice(["🪨 Камень 🪨", "✂️Ножницы ✂️", "📄 Бумага 📄"])
        if bot_choice == message.text:
            await message.answer(f"Бот тоже выбрал {bot_choice}, выходит, что ничья? Давайте еще раз попробуем!",
                                 reply_markup=new_kb)
            USERS[message.from_user.id]["tie"] += 1
            USERS[message.from_user.id]["in_game"] = False
        else:
            if (bot_choice == "🪨 Камень 🪨" and message.text == "✂️Ножницы ✂️")\
                or (bot_choice == "✂️Ножницы ✂️" and message.text == "📄 Бумага 📄") or \
                    (bot_choice == "📄 Бумага 📄" and message.text == "🪨 Камень 🪨"):
                await message.answer(f"Бот выбрал {bot_choice}. Вы проиграли\nМожет, еще сыграем?", reply_markup=new_kb)
                USERS[message.from_user.id]["bot_wins"] += 1
                USERS[message.from_user.id]["in_game"] = False
            else:
                await message.answer(f"Бот выбрал {bot_choice}. Вы победили! Сыграем еще разок?", reply_markup=new_kb)
                USERS[message.from_user.id]["user_wins"] += 1
                USERS[message.from_user.id]["in_game"] = False
    else:
        await message.reply("А мы с вами и не играем. Хотите сыграть?")


@dp.message_handler()  # хэндлер реагирующий на любые другие сообщения
async def process_all(message: types.Message):
    await message.answer("Я довольно ограниченный бот. Может, просто сыграем в игру?", reply_markup=new_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
