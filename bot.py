import logging
from api import API

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'Token here'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Init bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by _mezgoodle_.", parse_mode='Markdown')


@dp.message_handler(commands=['token'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    print(message.text)
    token = message.text.split(' ')[1]
    info = API(token)
    await message.reply(info.get_user_info(), parse_mode='Markdown')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
