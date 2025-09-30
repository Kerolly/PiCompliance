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

def load_data():
    with open("scan_results.json", "r", encoding="utf-8") as f:
        return json.load(f)

def is_pc(item: dict) -> bool:
    hostname = (item.get("hostname") or "").upper()
    ports = [p["port"] for p in item.get("ports", [])]
    return hostname.startswith("DESKTOP-") or hostname.startswith("LAPTOP-") or any(p in [135, 139, 445] for p in ports)

def is_phone(item: dict) -> bool:
    vendor = (item.get("vendor") or "").lower()
    phone_vendors = ["samsung", "apple", "huawei", "xiaomi", "oneplus", "cloud network technology"]
    return any(v in vendor for v in phone_vendors)

@app.get("/pc")
def get_pc():
    data = load_data()
    pc_items = [item for item in data if is_pc(item)]
    return JSONResponse(content=pc_items)

@app.get("/phone")
def get_phone():
    data = load_data()
    phone_items = [item for item in data if is_phone(item)]
    return JSONResponse(content=phone_items)

@app.get("/others")
def get_others():
    data = load_data()
    others_items = [item for item in data if not (is_pc(item) or is_phone(item))]
    return JSONResponse(content=others_items)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
