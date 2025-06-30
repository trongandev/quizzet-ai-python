import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # Mặc định là 8000 cho FastAPI
    uvicorn.run(app, host="0.0.0.0", port=port)