from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from moviepy import (
    ImageClip,
    ColorClip,
    CompositeVideoClip,
    concatenate_videoclips,
)

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
    r = requests.get(url, timeout=30)
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

        print(f"Descargando: {nombre}")

        descargar_imagen(url, nombre)

        archivos.append(nombre)

    clips = []

    for archivo in archivos:

        print(f"Procesando: {archivo}")

       imagen = (
    ImageClip(archivo)
    .resized(height=480)
    .with_duration(2)
    .with_position("center")
    .resized(lambda t: 1 + 0.08 * t)
)
`

        fondo = (
            ColorClip(
                size=(480, 854),
                color=(0, 0, 0)
            )
            .with_duration(2)
        )

        clip = CompositeVideoClip(
            [fondo, imagen],
            size=(480, 854)
        )

        clips.append(clip)

    print("Uniendo clips...")

    video = concatenate_videoclips(clips)

    nombre_video = f"{uuid.uuid4()}.mp4"

    print(f"Generando video: {nombre_video}")

    video.write_videofile(
        nombre_video,
        fps=6,
        codec="libx264"
    )

    print("Video generado correctamente")

    return FileResponse(
        nombre_video,
        media_type="video/mp4",
        filename="video.mp4"
    )
