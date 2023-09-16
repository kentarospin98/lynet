import aiohttp
from config import ai_21_api_key

client = aiohttp.ClientSession()


async def generate(
    prompt,
    model="j2-light",
    num_results=1,
    max_tokens=50,
    temprature=0.7,
    top_k_return=0,
    top_p=1,
    count_penalty=0,
    frequency_penalty=0,
    presence_penalty=0,
    stop_requences=["###", "\n"],
):
    url = f"https://api.ai21.com/studio/v1/{model}/complete"
    headers = {
        "Authorization": "Bearer " + ai_21_api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "numResults": num_results,
        "maxTokens": max_tokens,
        "temperature": temprature,
        "topKReturn": top_k_return,
        "topP": top_p,
        "countPenalty": {
            "scale": count_penalty,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False,
        },
        "frequencyPenalty": {
            "scale": frequency_penalty,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False,
        },
        "presencePenalty": {
            "scale": presence_penalty,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False,
        },
        "stopSequences": stop_requences,
    }
    async with client.post(url, headers=headers, json=payload) as resp:
        return await resp.json()
