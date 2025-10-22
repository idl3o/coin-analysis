from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/api/test")
def test():
    return {"status": "ok", "message": "API is working!"}

handler = Mangum(app)
