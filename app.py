import os
import time

from twitchio.ext import commands

from config import access_token, client_secret, db
import gpt


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=access_token,
            client_secret=client_secret,
            prefix="?",
            initial_channels=["stepsisshanti"],
        )

    async def event_ready(self):
        print(f"Logged in as {self.nick}")
        print(f"User id is {self.user_id}")

    def get_user_info_from_message(self, message):
        if not message.echo:
            return {
                "display_name": message.author.display_name,
                "id": message.author.id,
                "mention": message.author.mention,
                "name": message.author.name,
            }
        else:
            return {
                "display_name": self.nick,
                "id": self.user_id,
                "mention": "@" + self.nick,
                "name": self.nick,
            }

    async def event_message(self, message):
        m_doc = {
            "message": message.content,
            "timestamp": message.timestamp.timestamp(),
            "user": self.get_user_info_from_message(message),
        }

        await db.messages.insert_one(m_doc)

        if message.echo:
            return

        resp = await gpt.generate(
            f"Bot is a rude bot. Bot likes to insult people. Bot makes outdated references. Bot also makes puns on people's names \n\n{message.author.name}:{message.content}\nBot:",
            stop_requences=["\n"],
            temprature=0.8,
            model="j2-light",
        )
        reply = resp["completions"][0]["data"]["text"]
        await message.channel.send(reply)
        print(
            message.author.name + ": " + message.content + "\n" + "BOT: " + reply + "\n"
        )
        await self.handle_commands(message)


bot = Bot()
bot.run()
