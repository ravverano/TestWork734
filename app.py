from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

port = int(os.getenv("PORT", 5080))
if __name__ == "__main__":
    uvicorn.run(app, port=port, host="0.0.0.0")
