import asyncio
import os
import random
import re
import subprocess
import time

from twitchio import Message
from twitchio.ext import commands
import utils
import gpt
import generations
from config import access_token, client_secret, db


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=access_token,
            client_secret=client_secret,
            prefix="?",
            initial_channels=["stepsisshanti", "poisonnivyyy98", "SpnFamee"],
        )
        self.stream_title_cache = {"last_updated": 0, "title": ""}

    async def event_ready(self):
        print(f"Logged in as {self.nick}")
        print(f"User id is {self.user_id}")

    async def save_user_message(self, message):
        m_doc = {
            "channel": message.channel.name,
            "message": message.content,
            "timestamp": message.timestamp.timestamp(),
            "user": await self.get_user_info_from_message(message),
        }

        await db.messages.insert_one(m_doc)

    async def save_bot_message(self, message, response):
        m_doc = {
            "channel": message.channel.name,
            "message": response,
            "timestamp": message.timestamp.timestamp(),
            "user": {
                "display_name": self.nick,
                "id": self.user_id,
                "mention": "@" + self.nick,
                "name": self.nick,
            },
        }

        await db.messages.insert_one(m_doc)

    async def get_user_info_from_message(self, message):
        return {
            "display_name": message.author.display_name,
            "id": message.author.id,
            "mention": message.author.mention,
            "name": message.author.name,
        }

    async def update_user_activity(self, message: Message):
        await db.users.update_one(
            {"id": message.author.id},
            {
                "$set": {
                    "last_active": message.timestamp.timestamp(),
                    **await self.get_user_info_from_message(message),
                }
            },
            upsert=True,
        )

    async def update_user_profile(self, user):
        ...

    async def event_message(self, message):
        if message.echo:
            return

        if message.content[0] == "?":
            await self.handle_commands(message)
            return

        await asyncio.gather(
            self.save_user_message(message), self.update_user_activity(message)
        )

        if random.random() < 1:
            await self.update_user_profile(message.author)

        if random.random() < 0.3:
            print("Generating Response: ", end="")
            response = await generations.general_response(
                await utils.get_stream_info(self, message.channel),
                utils.get_current_song(),
                message,
            )
            print(response)
            await asyncio.gather(
                self.save_bot_message(message, response),
                message.channel.send(response),
            )

    @commands.command()
    async def clear_history(self, ctx: commands.Context):
        if ctx.channel.name != ctx.author.name:
            await ctx.send(f"Uhmmm... You're not allowed to this this, {ctx.author.name}!")
            return
        
        await db.messages.delete_many({"channel": ctx.channel.name})
        await ctx.send(f"Chat history is clean, {ctx.author.name}!")


bot = Bot()
bot.run()
