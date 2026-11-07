from fastapi import FastAPI

app = FastAPI(title = "ComunicAI")

@app.get("/health")
def health():
    return {"status":"ok"}