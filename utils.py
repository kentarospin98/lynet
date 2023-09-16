import re
import subprocess
import time


current_song_cache = {}
stream_info_cache = {}
channel_user_cache = {}


def get_current_song():
    global current_song_cache

    if current_song_cache.get("last_updated", 0) > time.time() - 10:
        return current_song_cache

    completed = subprocess.run(
        ["playerctl", "metadata"], capture_output=True, text=True
    )
    match = re.search(re.compile(".*:title\s*(.*)"), completed.stdout)
    if match is None:
        song = {"playing": False, "title": "No Song Playing"}
    else:
        song = {"playing": True, "title": match[1]}
    song["last_updated"] = time.time()
    current_song_cache = song
    return song


async def get_channel_user(channel):
    cache = channel_user_cache.get(channel.name, {})
    if cache.get("last_updated", 0) > time.time() - 120:
        return cache

    user = await channel.user()
    user_doc = {
        "display_name": user.display_name,
        "id": user.user_id,
        "mention": user.mention,
        "name": user.name,
    }
    user_doc["last_updated"] = time.time()
    return user_doc


async def get_stream_info(bot, channel):
    global stream_info_cache
    if stream_info_cache.get("last_updated", 0) > time.time() - 60:
        return stream_info_cache
    channel = await bot.fetch_channel(channel.name)
    if channel is None:
        channel_info = {
            "title": "Not Streaming",
            "game_name": "Not Streaming",
            "game_id": -1,
        }
    else:
        channel_info = {
            "title": channel.title,
            "game_name": channel.game_name,
            "game_id": channel.game_id,
        }
    channel_info["last_updated"] = time.time()
    stream_info_cache = channel_info
    return channel_info
