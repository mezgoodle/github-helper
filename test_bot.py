from unittest import IsolatedAsyncioTestCase

import aiohttp

from bot import bot
from config import API_TOKEN


class TestBot(IsolatedAsyncioTestCase):
    async def test_bot_auth(self):
        bot._session = aiohttp.ClientSession()
        bot_info = await bot.get_me()
        await bot._session.close()
        self.assertEqual(bot_info["username"], "github_helperbot")
