from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn

app = FastAPI()

# allow Angular dev server
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_credentials=True,   
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/data")
def get_data():
    with open("scan_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse(content=data)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
