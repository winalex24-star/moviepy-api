from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()


class VideoRequest(BaseModel):
    titulo: str
    audio_url: str
    imagen1: str
    imagen2: str
    imagen3: str
    imagen4: str
    imagen5: str


def descargar_audio(url, archivo):

    print("================================")
    print("AUDIO URL:")
    print(url)

    r = requests.get(
        url,
        timeout=60,
        allow_redirects=True
    )

    print("STATUS CODE:")
    print(r.status_code)

    print("CONTENT TYPE:")
    print(r.headers.get("content-type"))

    r.raise_for_status()

    with open(archivo, "wb") as f:
        f.write(r.content)

    print("TAMANO AUDIO:")
    print(os.path.getsize(archivo))

    print("================================")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/video")
def create_video(req: VideoRequest):

    audio_file = "audio.mp3"

    descargar_audio(
        req.audio_url,
        audio_file
    )

    with open(audio_file, "rb") as f:
        primeros_bytes = f.read(300)

    print("PRIMEROS BYTES:")
    print(primeros_bytes)

    return {
        "titulo": req.titulo,
        "audio_url": req.audio_url,
        "size": os.path.getsize(audio_file),
        "primeros_bytes": str(primeros_bytes[:100])
    }
