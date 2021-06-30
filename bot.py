# TODO: look for api elements and add logic to the bot
import logging
import os
from typing import Tuple

from github.Repository import Repository

from api import Api
from database import Client
from hashing import Hasher
from config import API_TOKEN, DB_PASSWORD

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from github.GithubException import BadCredentialsException, GithubException

# CONSTANTS
CLOSE = 'c'
MERGE = 'm'
CREATE_ISSUE = 'i'
CREATE_PR = 'p'


class Issue(StatesGroup):
    RepoName = State()
    Title = State()
    Body = State()
    Assignee = State()
    Repository = State()


class PullRequest(StatesGroup):
    RepoName = State()
    Title = State()
    Body = State()
    Assignee = State()
    Base = State()
    Head = State()
    Draft = State()
    Repository = State()


# Configure logging
logging.basicConfig(level=logging.INFO)

# Init bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def decrypt_token(user_id: int) -> str:
    """
    Method for decrypting token from the database
    :param user_id: user id in Telegram
    :return: decrypted token
    """
    db = Client(DB_PASSWORD, 'githubhelper', 'tokens')
    data = db.get({'telegram_id': user_id})
    hasher = Hasher(os.getenv('KEY', b'Kt7ioOW4eugqDkfqcYiCz2mOuyiWRg_MTzckxEVp978='))
    try:
        encrypted_token = data.get('token')
        decrypted_token = hasher.decrypt_message(encrypted_token)
        return decrypted_token
    except TypeError:
        return ''


async def get_full_repo(repo: Repository) -> Tuple[str, types.InlineKeyboardMarkup]:
    """
    Function for returning pretty information about repository
    :param repo: object with data about Repository
    :return: text and keyboard with buttons
    """
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(types.InlineKeyboardButton('Create issue', callback_data=f'i{repo.name}'))
    inline_keyboard.add(types.InlineKeyboardButton('Create pull request', callback_data=f'p{repo.name}'))
    for issue in repo.get_issues():
        if not issue.pull_request:
            button = types.InlineKeyboardButton(f'Issue #{issue.number} - {issue.title}', url=issue.html_url)
        else:
            button = types.InlineKeyboardButton(f'Pull request #{issue.number} - {issue.title}',
                                                url=issue.html_url)
        inline_keyboard.add(button)
    final_text = f'Name: *{repo.name}*\nLink: [click here]({repo.html_url})\n' \
                 f'Stars: *{repo.stargazers_count}*\nTotal issues and prs: *{repo.get_issues().totalCount}*'
    return final_text, inline_keyboard


async def prepare_issues_or_prs(token: str, option: bool) -> Tuple[str, types.InlineKeyboardMarkup]:
    """
    Function for returning pretty information about issues or pull requests
    :param token: decrypted GitHub token
    :param option: issue or pull request
    :return: text and keyboard with buttons
    """
    info = Api(token)
    items = info.get_issues_or_prs(option)
    final_text = ''
    index = 1
    buttons = []
    length_of_url = 29
    inline_keyboard = types.InlineKeyboardMarkup(row_width=4)
    for item in items:
        final_text += f'*{index}* _{item.title}_ [#{item.number}]({item.html_url}). ' \
                      f'[Link to repository]({item.repository.html_url}). Created: _{item.created_at}_. ' \
                      f'Author: _{item.user.name}_\n'
        url = item.url[length_of_url:]
        button = types.InlineKeyboardButton(f'Close {index}', callback_data=f'c{url}')
        buttons.append(button)
        if not option:
            button = types.InlineKeyboardButton(f'Merge {index}', callback_data=f'm{url}')
            buttons.append(button)
        index += 1
    inline_keyboard.add(*buttons)
    return final_text, inline_keyboard


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = callback_query.from_user.id
    decrypted_token = await decrypt_token(user_id)
    if decrypted_token:
        info = Api(decrypted_token)
        if callback_query.data.startswith(CLOSE):
            if info.close_issues_or_prs(callback_query.data[len(CLOSE):]):
                return await bot.answer_callback_query(callback_query.id, 'Issue has been closed')
            else:
                return await bot.answer_callback_query(callback_query.id, 'Error while closing')
        elif callback_query.data.startswith(MERGE):
            if info.merge_prs(callback_query.data[len(MERGE):]):
                return await bot.answer_callback_query(callback_query.id, 'Pull request has been merged')
            else:
                return await bot.answer_callback_query(callback_query.id, 'Error while merging')
        elif callback_query.data.startswith(CREATE_ISSUE):
            await Issue.first()
            await bot.send_message(callback_query.from_user.id, 'So, the name of repository is:')
            message = await bot.send_message(callback_query.from_user.id, callback_query.data[1:])
            message.from_user.id = callback_query.from_user.id
            return await handle_complex_state(message, dp.current_state(), Issue, 'Write the title of issue',
                                              'Enter valid name of repository', 'RepoName')
        elif callback_query.data.startswith(CREATE_PR):
            await PullRequest.first()
            await bot.send_message(callback_query.from_user.id, 'So, the name of repository is:')
            message = await bot.send_message(callback_query.from_user.id, callback_query.data[1:])
            message.from_user.id = callback_query.from_user.id
            return await handle_complex_state(message, dp.current_state(), PullRequest,
                                              'Write the title of pull request',
                                              'Enter valid name of repository', 'RepoName')
        else:
            data = info.get_repo(callback_query.data)
            final_text, inline_keyboard = await get_full_repo(data)
            return await bot.send_message(callback_query.from_user.id, final_text, reply_markup=inline_keyboard,
                                          parse_mode='Markdown')
    else:
        return await bot.send_message(callback_query.from_user.id,
                                      'Your token isn\'t in database. Type the command /token')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    return await message.reply("Hi!\nI'm EchoBot!\nPowered by _mezgoodle_.", parse_mode='Markdown')


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    text = 'Here you can see all instructions:\n' \
           '/token - set your <i>GitHub token</i>. Example: /token your_github_token\n' \
           '/me - get information about the user\n' \
           '/prs - get information about user pull requests\n' \
           '/issues - get information about user issues\n' \
           '/repos - get information about user repositories\n' \
           '/create_issues - start the process of creating an issue. Just answer the questions.\n' \
           '/create_pr - start the process of creating a pull request. Just answer the questions.\n' \
           'Also you can just type the name of repository and get information.'
    return await message.reply(text, parse_mode='Html')


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
    hasher = Hasher(os.getenv('KEY', b'Kt7ioOW4eugqDkfqcYiCz2mOuyiWRg_MTzckxEVp978='))
    user_id = message.from_user.id
    try:
        info.get_user_info()
    except BadCredentialsException:
        return await message.reply('*Bad* credentials', parse_mode='Markdown')
    db = Client(DB_PASSWORD, 'githubhelper', 'tokens')
    data = db.get({'telegram_id': user_id})
    encrypted_token = hasher.encrypt_message(token)
    if data:
        db.update({'telegram_id': user_id}, {'token': encrypted_token})
        await message.reply('Your token has been _updated_', parse_mode='Markdown')
    else:
        db.insert({'token': encrypted_token, 'telegram_id': user_id})
        await message.reply('Your token has been _set_', parse_mode='Markdown')
    return await message.answer(info.get_user_info(), parse_mode='Markdown')


@dp.message_handler(commands=['me'])
async def get_me(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    if decrypted_token:
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
    decrypted_token = await decrypt_token(user_id)
    if decrypted_token:
        info = Api(decrypted_token)
        repos = info.get_repos()
        text = ''
        index = 1
        inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
        buttons = []
        for repo in repos:
            if not repo.archived:
                text += f'{index}. {repo.name}. [Link]({repo.html_url}). ' \
                        f'Total issues and prs: {repo.get_issues().totalCount}\n' \
                        f'Type: _{"Private" if repo.private else "Public"}_\n'
                button = types.InlineKeyboardButton(str(index), callback_data=repo.name)
                buttons.append(button)
                index += 1
        inline_keyboard.add(*buttons)
        text += '\nClick the number of repository to get *details*'
        return await message.answer(text, parse_mode='Markdown', reply_markup=inline_keyboard)
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


@dp.message_handler(commands=['issues'])
async def get_issues(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    if decrypted_token:
        final_text, inline_keyboard = await prepare_issues_or_prs(decrypted_token, True)
        return await message.answer(final_text, parse_mode='Markdown', reply_markup=inline_keyboard)
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


# TODO: show passing workflows
@dp.message_handler(commands=['prs'])
async def get_prs(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    if decrypted_token:
        final_text, inline_keyboard = await prepare_issues_or_prs(decrypted_token, False)
        return await message.answer(final_text, parse_mode='Markdown', reply_markup=inline_keyboard)
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


@dp.message_handler(commands=['create_issue'], state=None)
async def create_issue(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    if decrypted_token:
        await Issue.first()
        await message.reply('You started the process of creating the issue. Please, answer the questions')
        return await message.answer('What is a name of repository?')
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


@dp.message_handler(commands=['create_pr'], state=None)
async def create_pr(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    if decrypted_token:
        await PullRequest.first()
        await message.reply('You started the process of creating the pull request. Please, answer the questions')
        return await message.answer('What is a name of repository?')
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    return await message.reply('Cancelled.')


async def handle_simple_state(message, state, state_class, key, answer_text):
    answer = message.text
    await state.update_data({key: answer})
    await state_class.next()
    return await message.answer(answer_text)


async def handle_complex_state(message, state, state_class, answer_text, error_text, key):
    answer = message.text
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    info = Api(decrypted_token)
    repo = info.get_repo(answer)
    if repo:
        await state.update_data({key: answer})
        await state.update_data(Repository=repo)
        await state_class.next()
        return await message.answer(answer_text)
    else:
        return await message.reply(error_text)


@dp.message_handler(state=Issue.RepoName)
async def answer_repo_name_issue(message: types.Message, state: FSMContext):
    return await handle_complex_state(message, state, Issue, 'Write the title of issue',
                                      'Enter valid name of repository', 'RepoName')


@dp.message_handler(state=PullRequest.RepoName)
async def answer_repo_name_pr(message: types.Message, state: FSMContext):
    return await handle_complex_state(message, state, PullRequest, 'Write the title of pull request',
                                      'Enter valid name of repository', 'RepoName')


@dp.message_handler(state=Issue.Title)
async def answer_title_issue(message: types.Message, state: FSMContext):
    return await handle_simple_state(message, state, Issue, 'Title', 'Write the body of issue')


@dp.message_handler(state=PullRequest.Title)
async def answer_title_pr(message: types.Message, state: FSMContext):
    return await handle_simple_state(message, state, PullRequest, 'Title', 'Write the body of pull request')


@dp.message_handler(state=Issue.Body)
async def answer_body_issue(message: types.Message, state: FSMContext):
    return await handle_simple_state(message, state, Issue, 'Body',
                                     'Write the nickname of user to assign this issue. If no-one - write empty')


@dp.message_handler(state=PullRequest.Body)
async def answer_body_pr(message: types.Message, state: FSMContext):
    return await handle_simple_state(message, state, PullRequest, 'Body',
                                     'Write the nickname of user to assign this pr. If no-one - write empty')


@dp.message_handler(state=PullRequest.Assignee)
async def answer_assign_pr(message: types.Message, state: FSMContext):
    if message.text == 'empty':
        message.text = ''
    return await handle_simple_state(message, state, PullRequest, 'Assignee', 'Write the name of the base branch')


# TODO: if empty assign
@dp.message_handler(state=Issue.Assignee)
async def answer_assign_issue(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'empty':
        await state.update_data(Assignee='')
    else:
        await state.update_data(Assignee=answer)
    data = await state.get_data()
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    info = Api(decrypted_token)
    issue = info.create_issue(data)
    await state.finish()
    if issue:
        return await message.answer('Issue has been created')
    else:
        return await message.answer('Error')


@dp.message_handler(state=PullRequest.Base)
async def answer_base_pr(message: types.Message, state: FSMContext):
    answer = message.text
    state_data = await state.get_data()
    if state_data.get('Repository').default_branch == answer:
        await state.update_data(Base=answer)
        await PullRequest.next()
        return await message.answer('Write the name of the head branch')
    else:
        return await message.reply('The name of the base branch is incorrect')


@dp.message_handler(state=PullRequest.Head)
async def answer_head_pr(message: types.Message, state: FSMContext):
    answer = message.text
    state_data = await state.get_data()
    try:
        state_data.get('Repository').get_branch(answer)
    except GithubException:
        return await message.reply('The name of the head branch is incorrect')
    await state.update_data(Head=answer)
    await PullRequest.next()
    return await message.answer('Is this pr still in draft?(Write True or False)')


@dp.message_handler(state=PullRequest.Draft)
async def answer_draft_pr(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.strip().lower() == 'true':
        await state.update_data(Draft=True)
    elif answer.strip().lower() == 'false':
        await state.update_data(Draft=False)
    data = await state.get_data()
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    info = Api(decrypted_token)
    pr = info.create_pr(data)
    await state.finish()
    if pr:
        return await message.answer('Pull request has been created')
    else:
        return await message.answer('Error')


@dp.message_handler()
async def echo(message: types.Message):
    user_id = message.from_user.id
    decrypted_token = await decrypt_token(user_id)
    if decrypted_token:
        info = Api(decrypted_token)
        data = info.get_repo(message.text)
        if data:
            final_text, inline_keyboard = await get_full_repo(data)
            return await message.answer(final_text, reply_markup=inline_keyboard, parse_mode='Markdown')
        else:
            return await message.answer('Couldn\'t find your repository')
    else:
        return await message.answer('Your token isn\'t in database. Type the command /token')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
