from config import db
import gpt
from twitchio import Message

user_info = {
    "name": "Sandra",
    "likes": ["Eating food", "Playing Retro Games", "Bollywood music"],
    "streams": ["Overwatch 2", "Catherine", "Programming"],
}


async def general_response(stream_info, song_info, message: Message):
    name = user_info["name"]
    prompt = f"""{name} is a polite twitch streamer. {name} like {', '.join(user_info['likes'])}. {name} streams {', '.join(user_info['streams'])}. {name} is really funny and likes to make jokes.
{name} is empathetic and always tries to be nice to everyone. {name} is on the Twitch Chat interacting with the viewers as they stream.

{name}'s Live stream has the title "{stream_info['title']}"
"""
    if song_info["playing"]:
        prompt += f'{name} is playing the song "{song_info["title"]}" on the stream.\n'
    else:
        prompt += f"{name} is not playing music on the stream.\n"

    prompt += "\n" + await get_transcript(message.channel.name)
    prompt += f"{name}: "

    resp = await gpt.generate(prompt, model="j2-ultra", frequency_penalty=0.6)
    if "completions" in resp:
        return resp["completions"][0]["data"]["text"]


async def get_transcript(channel):
    messages = db.messages.find(
        {"channel": channel}, sort=[("timestamp", -1)], limit=10
    )
    transcript = ""
    async for message in messages:
        transcript += f"{message['user']['display_name']}: {message['message']}\n"

    return transcript
