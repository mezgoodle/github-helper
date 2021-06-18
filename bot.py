import logging
from api import Api
from database import Client
from hashing import Hasher

from aiogram import Bot, Dispatcher, executor, types
from github.GithubException import BadCredentialsException

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
async def get_token(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    token = message.text.split(' ')[1]
    info = Api(token)
    hasher = Hasher()
    user_id = message.from_user.id
    try:
        info.get_user_info()
    except BadCredentialsException:
        return await message.reply('*Bad* credentials', parse_mode='Markdown')
    db = Client('password')
    data = db.get({'telegram_id': user_id})
    encrypted_token = hasher.encrypt_message(token)
    if data:
        db.update({'telegram_id': user_id}, {'token': encrypted_token})
        await message.reply('Your token has been _updated_', parse_mode='Markdown')
    else:
        db.insert({'token': encrypted_token, 'telegram_id': user_id})
        await message.reply('Your token has been _set_', parse_mode='Markdown')
    await message.answer(info.get_user_info(), parse_mode='Markdown')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
