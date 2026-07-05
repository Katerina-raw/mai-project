from fastapi import FastAPI
from pydantic import BaseModel

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
    return {"status": "success",
            "message": "Successfully done"}

