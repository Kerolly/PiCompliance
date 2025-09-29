def get_vendor(mac, oui_file="pi_scripts/nmap_oui_database.txt"):
    prefix = mac.replace(":", "").replace("-", "").upper()[:6]

    try:
        with open(oui_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.split(None, 1)
                file_prefix = parts[0].replace("-", "").upper()
                if file_prefix == prefix:
                    return parts[1].strip()
                
    except FileNotFoundError:
        return f"File {oui_file} not found"
    except Exception as e:
        return f"[Error]: {e}"

    return "Unknown"


print(get_vendor("60-E9-AA-2B-7D-31"))
