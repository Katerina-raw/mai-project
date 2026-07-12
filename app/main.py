from fastapi import FastAPI
from pydantic import BaseModel

from app.ai import request_to_qwen
from app.utiles import decode_base64_data, encode_base64_data
from app.utiles import extract_zip_data

app = FastAPI()

class Subject(BaseModel):
    ID: int
    Lecture_hours: int
    Practice_hours: int
    Lab_hours: int
    Subject_name: str
    Subject_description: str
    Blocks: list[dict]
    Archives: bytes

@app.get("/v1")
def register(subject: Subject):
    bytes_archives = decode_base64_data(subject.Archives)
    data = extract_zip_data(bytes_archives)
    response = request_to_qwen(data, subject.Lecture_hours)

    return {"status": "success",
            "message": "Successfully done"}

