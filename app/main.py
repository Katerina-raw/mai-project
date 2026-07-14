from fastapi import FastAPI
from pydantic import BaseModel

from app.ai import AI
from app.utiles import decode_base64_data, encode_base64_data
from app.utiles import extract_zip_data

app = FastAPI()

class Subject(BaseModel):
    ID: int
    Subject_name: str
    Subject_description: str
    Blocks: list[dict]
    Archives: bytes

@app.get("/v1")
def register(subject: Subject):
    bytes_archives = decode_base64_data(subject.Archives)
    data = extract_zip_data(bytes_archives)
    ai = AI()
    return {"status": "success",
            "message": "Successfully done",
            "answer": ai.orchestrate_course_generation(subject.Blocks, data)}

