from fastapi import FastAPI

app = FastAPI(title="Novin Social API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "novin-social-api"}


@app.get("/")
def root():
    return {
        "name": "Novin Social",
        "version": "0.1.0",
        "mode": "multi-project social sales platform",
    }
