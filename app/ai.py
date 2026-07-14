import json
import os

import requests
from app.prompts import system_prompt

API_KEY = "" # os.getenv("AI_API_KEY")


class AI:
    def __init__(self):
        self.API_KEY = "" # os.getenv("AI_API_KEY")

    def request_to_qwen(self, data: dict, system_prompt) -> dict:
        print(1)
        headers = {
            "Authorization": "Bearer {}".format(self.API_KEY),
            "Content-Type": "application/json"
        }
        response = requests.post(
            'https://api.ai.mai.ru/v1/chat/completions',
            headers=headers,
            json={
                "model": "Qwen3.5-122B-A10B",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": str(data)}]})

        abc = response.json()
        abc = abc['choices'][0]['message']['content']
        thinking_end = abc.index('</think>') + len('</think>')
        return json.loads(abc[thinking_end:])

    def orchestrate_course_generation(self, blocks: dict, files_data) -> list:
        res = []

        for block in blocks:
            res.append({
                      "block_name": block["block_name"],
                      "Lecture_hours": block["Lecture_hours"],
                      "Practice_hours": block["Practice_hours"],
                      "Lab_hours": block["Lab_hours"]})

            block["Lecture_hours"] //= 2
            block["Practice_hours"] //= 2
            block["Lab_hours"] //= 2
            block["data"] = files_data

            response = self.request_to_qwen(block, system_prompt)

            res[-1]["chapters"] = response["chapters"]

        return res


