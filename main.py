from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class VideoRequest(BaseModel):
    titulo: str
    imagen1: str
    imagen2: str
    imagen3: str
    imagen4: str
    imagen5: str

@app.get("/")
def health():
    return {
        "status": "ok"
    }

@app.post("/video")
def create_video(req: VideoRequest):

    return {
        "status": "ok",
        "titulo": req.titulo,
        "imagenes": [
            req.imagen1,
            req.imagen2,
            req.imagen3,
            req.imagen4,
            req.imagen5
        ]
    }
