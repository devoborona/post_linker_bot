import configparser
import logging

from aiogram import Bot, Dispatcher, executor, types, filters

# Режим роботи бота за замовчанням - TEST,
# щоб перейти на режим PROD, замініть 1 на 0
mode = ['PROD', 'TEST'][1]

# Робота з конфіг файлом
config = configparser.ConfigParser()
config.read('config.ini')

# Присвоєння змінним даних з файлу конфігурації
API_TOKEN = config[mode]['API_TOKEN']
CNL = config[mode]['CNL']
ADMIN_ID = config[mode]['ADMIN_ID']

# Посилання для ваших постів
# '<a href="ваше_посилання">текст посилання</a>'
LINK = '<a href="https://t.me/+VctHAAqFS0Y0NmRi">МЕМОБОРОНА</a>'

# Вмикаємо лог
logging.basicConfig(level=logging.INFO)

# Створюємо обʼєкт бота, диспетчера, фільтр перевірки
bot = Bot(token=API_TOKEN, parse_mode='html')
dp = Dispatcher(bot)
admin_check = filters.AdminFilter(is_chat_admin=CNL)


async def start_bot(_):
    """
    Відправляє адмінам повідомлення про запуск бота
    :param _:
    :return: None
    """
    await bot.send_message(ADMIN_ID, f'Бот працює в режимі {mode}.')


@dp.message_handler(admin_check, commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Відповідає на команди `/start` або `/help`
    """
    await message.reply("Привіт, я мем-майор Ботенко🫡")


@dp.message_handler(admin_check, content_types=types.ContentType.PHOTO)
async def photo_linker(message: types.Message):
    """
    Додає посилання до картинок
    """
    if message.caption:
        caption_and_link = f'{message.caption} \n\n {LINK}'
    else:
        caption_and_link = LINK

    await bot.send_photo(chat_id=CNL, photo=message.photo[-1].file_id, caption=caption_and_link)


@dp.message_handler(admin_check, content_types=types.ContentType.VIDEO)
async def video_linker(message: types.Message):
    """
    Додає посилання до відео
    """
    if message.caption:
        caption_and_link = f'{message.caption} \n\n {LINK}'
    else:
        caption_and_link = LINK

    await bot.send_video(chat_id=CNL, video=message.video.file_id, caption=caption_and_link)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot)