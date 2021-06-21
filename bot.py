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
    try:
        token = message.text.split(' ')[1]
    except IndexError:
        return await message.reply('Enter the _token_', parse_mode='Markdown')
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


@dp.message_handler(commands=['me'])
async def get_me(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    db = Client('password')
    data = db.get({'telegram_id': user_id})
    hasher = Hasher()
    if data:
        encrypted_token = data.get('token')
        decrypted_token = hasher.decrypt_message(encrypted_token)
        info = Api(decrypted_token)
        return await message.answer(info.get_user_info(), parse_mode='Markdown')
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


@dp.message_handler(commands=['repos'])
async def get_repos(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    db = Client('password')
    data = db.get({'telegram_id': user_id})
    hasher = Hasher()
    if data:
        encrypted_token = data.get('token')
        decrypted_token = hasher.decrypt_message(encrypted_token)
        info = Api(decrypted_token)
        repos = info.get_repos()
        text = ''
        index = 1
        for repo in repos:
            if not repo.archived:
                text += f'{index}. {repo.name}. [Link]({repo.html_url}). ' \
                          f'Total issues and prs: {repo.get_issues().totalCount}\n'
                index += 1
        return await message.answer(text, parse_mode='Markdown')
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


@dp.message_handler(commands=['issues'])
async def get_issues(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    db = Client('zxcVBN0911<>')
    data = db.get({'telegram_id': user_id})
    hasher = Hasher()
    if data:
        encrypted_token = data.get('token')
        decrypted_token = hasher.decrypt_message(encrypted_token)
        info = Api(decrypted_token)
        return await message.answer(info.get_issues(), parse_mode='Markdown')
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


@dp.message_handler()
async def echo(message: types.Message):
    user_id = message.from_user.id
    db = Client('password')
    hasher = Hasher()
    data = db.get({'telegram_id': user_id})
    encrypted_token = data.get('token')
    decrypted_token = hasher.decrypt_message(encrypted_token)
    info = Api(decrypted_token)
    data = info.get_repo(message.text)
    if data:
        inline_keyboard = types.InlineKeyboardMarkup()
        for issue in data['issues']:
            if not issue.pull_request:
                button = types.InlineKeyboardButton(f'Issue #{issue.number} - {issue.title}', url=issue.html_url)
            else:
                button = types.InlineKeyboardButton(f'Pull request #{issue.number} - {issue.title}', url=issue.html_url)
            inline_keyboard.add(button)
        final_text = f"Name: *{data['name']}*\nLink: [click here]({data['url']})\n" \
                     f"Stars: *{data['stars']}*\nTotal issues and prs: *{data['count_of_issues']}*"
        await message.answer(final_text, reply_markup=inline_keyboard, parse_mode='Markdown')
    else:
        await message.answer('Couldn\'t find your repository')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
