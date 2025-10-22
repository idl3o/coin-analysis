from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI(title="Crypto Analysis API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Crypto Analysis API", "status": "running", "version": "1.0.0"}

@app.get("/test")
async def test():
    return {"status": "ok", "message": "Minimal test endpoint working!"}

# Mangum handler for Vercel
handler = Mangum(app)
