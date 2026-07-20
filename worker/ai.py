import json

import requests
from worker.prompts import system_prompt

API_KEY = "" # os.getenv("AI_API_KEY")

class AI:
    def __init__(self):
        self.API_KEY = "" # os.getenv("AI_API_KEY")

    def request_to_qwen(self, data: dict, prompt:str) -> dict:
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
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": str(data)}]})

        abc = response.json()
        abc = abc['choices'][0]['message']['content']
        return json.loads(abc)

    def orchestrate_course_generation(self, blocks: dict, files_data) -> list:
        res = []

        for block in blocks:
            res.append({
                      "block_name": block["block_name"],
                      "lecture_hours": block["lecture_hours"],
                      "practice_hours": block["practice_hours"],
                      "lab_hours": block["lab_hours"]})

            block["lecture_hours"] //= 2
            block["practice_hours"] //= 2
            block["lab_hours"] //= 2
            block["data"] = files_data

            response = self.request_to_qwen(block, system_prompt)

            res[-1]["chapters"] = response["chapters"]

        return res


