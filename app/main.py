from fastapi import FastAPI
from pydantic import BaseModel
from app.utiles import decode_base64_data
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
    archives = subject.Archives
    bytes_archives = decode_base64_data(archives)
    data = extract_zip_data(bytes_archives)
    return {"status": "success",
            "message": "Successfully done",
            "answer": data }

