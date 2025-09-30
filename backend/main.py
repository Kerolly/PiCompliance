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
    """Identifică PC-uri/laptop-uri pe baza hostname-ului, OS-ului și porturilor specifice Windows/Linux"""
    hostname = (item.get("hostname") or "").upper()
    ports = [p["port"] for p in item.get("ports", [])]
    os_info = item.get("os", [])
    vendor = (item.get("vendor") or "").lower()
    
    # Hostname-uri specifice PC
    if (hostname.startswith("DESKTOP-") or 
        hostname.startswith("LAPTOP-") or 
        hostname.startswith("PC-") or
        any(name in hostname for name in ["WORKSTATION", "COMPUTER"])):
        return True
    
    # Porturi specifice Windows (SMB, NetBIOS, RPC)
    windows_ports = [135, 139, 445, 1433, 3389, 5985, 5986]
    if any(p in windows_ports for p in ports):
        return True
    
    # OS detection
    if os_info:
        for os_entry in os_info:
            os_match = (os_entry.get("os_match") or "").lower()
            if any(os_name in os_match for os_name in ["windows", "linux", "ubuntu", "debian", "centos", "fedora", "arch"]):
                return True
    
    # Vendor-uri specifice PC/laptop
    pc_vendors = ["intel", "amd", "nvidia", "dell", "hp", "lenovo", "asus", "msi", "gigabyte", "asrock"]
    if any(v in vendor for v in pc_vendors):
        return True
    
    return False


def is_phone(item: dict) -> bool:
    """Identifică telefoane mobile pe baza OS-ului, vendor-ului și porturilor specifice"""
    vendor = (item.get("vendor") or "").lower()
    os_info = item.get("os", [])
    ports = [p["port"] for p in item.get("ports", [])]
    
    # Vendor-uri specifice telefoane
    phone_vendors = [
        "samsung", "apple", "huawei", "xiaomi", "oneplus", "oppo", "vivo", 
        "motorola", "lg", "sony", "nokia", "google", "realme", "honor",
        "cloud network technology"  # pentru unele dispozitive chinezești
    ]
    
    if any(v in vendor for v in phone_vendors):
        return True
    
    # OS detection pentru mobile
    if os_info:
        for os_entry in os_info:
            os_match = (os_entry.get("os_match") or "").lower()
            family = (os_entry.get("family") or "").lower()
            
            # iOS detection
            if ("ios" in os_match or "darwin" in os_match or 
                "iphone" in os_match or "ipad" in os_match or
                family == "ios"):
                return True
            
            # Android detection
            if ("android" in os_match or family == "android"):
                return True
    
    # Porturi specifice dispozitivelor mobile (AirPlay, screen sharing, etc.)
    mobile_ports = [62078, 49152, 5353, 7000, 7001]
    if any(p in mobile_ports for p in ports) and len(ports) <= 3:
        return True
    
    return False


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


@app.get("/all-categorized")
def get_all_categorized():
    """Returnează toate dispozitivele cu categoria lor"""
    data = load_data()
    categorized_data = []
    
    for item in data:
        item_copy = item.copy()
        if is_pc(item):
            item_copy["category"] = "PC/Laptop"
        elif is_phone(item):
            item_copy["category"] = "Phone/Mobile"
        else:
            item_copy["category"] = "Others"
        
        categorized_data.append(item_copy)
    
    return JSONResponse(content=categorized_data)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
