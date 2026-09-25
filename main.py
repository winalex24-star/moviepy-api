from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "moviepy-api",
        "version": "1.0"
    }

@app.post("/video")
def create_video():
    return {
        "message": "Video endpoint funcionando"
    }
