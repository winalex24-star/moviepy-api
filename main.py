from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from moviepy import ImageClip, concatenate_videoclips
import requests
import uuid

app = FastAPI()

class VideoRequest(BaseModel):
    titulo: str
    imagen1: str
    imagen2: str
    imagen3: str
    imagen4: str
    imagen5: str

def descargar_imagen(url, archivo):
    r = requests.get(url)
    r.raise_for_status()

    with open(archivo, "wb") as f:
        f.write(r.content)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/video")
def create_video(req: VideoRequest):

    imagenes = [
        req.imagen1,
        req.imagen2,
        req.imagen3,
        req.imagen4,
        req.imagen5,
    ]

    archivos = []

    for i, url in enumerate(imagenes):
        nombre = f"img_{i}.jpg"

        descargar_imagen(url, nombre)

        archivos.append(nombre)

    clips = []

    for archivo in archivos:
        clip = (
            ImageClip(archivo)
            .resized(height=720)
            .with_duration(2)
        )

        clips.append(clip)

    video = concatenate_videoclips(clips)

    nombre_video = f"{uuid.uuid4()}.mp4"

    video.write_videofile(
        nombre_video,
        fps=12,
        codec="libx264"
    )

    return FileResponse(
        nombre_video,
        media_type="video/mp4",
        filename="video.mp4"
    )
