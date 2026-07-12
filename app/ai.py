import json
import os

import requests
from app.prompts import system_prompt_lecture

API_KEY = "" # os.getenv("AI_API_KEY")

def request_to_qwen(data: dict, hour: int) -> dict:
    hour //= 2
    data['lecture_hours'] = hour

    headers = {
        "Authorization": "Bearer {}".format(API_KEY),
        "Content-Type": "application/json"
    }
    response = requests.post(
        'https://api.ai.mai.ru/v1/chat/completions',
        headers=headers,
        json={
            "model": "Qwen3.5-122B-A10B",
            "messages": [
                {"role": "system", "content": system_prompt_lecture},
                {"role": "user", "content": str(data)}]})
    abc = response.json()
    abc = abc['choices'][0]['message']['content']
    thinking_end = abc.index('</think>') + len('</think>')
    return json.loads(abc[thinking_end:])

