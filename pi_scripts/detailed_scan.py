import nmap
import socket
from admin_privileges import ensure_elevated

ensure_elevated()

def get_device_info(ip):
    scanner = nmap.PortScanner()
    options = "-sS -sV -O -Pn --host-timeout 30s -T4 --open --top-ports 1000" 

    print(f"\n---> Starting detailed scan for: {ip} ...")
    print("...")
    print("---> this may take a while ....")

    try:
        scanner.scan(ip, arguments=options)
    except nmap.PortScannerError as e:
        print(f"Error, scan failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    host = ip

    if host not in scanner.all_hosts():
        print(f"No information found for {host}")
        return None, []
    else:
        # General info
        print("Host: ", host)
        host_info = scanner[host]
        print("State: ", host_info.state())

        # --- OS Detection NMAP ---
        os_info = get_os_namp(host_info)
        if not os_info:
            print("No high-accuracy OS information available, continuing with port scan...")

        # --- Ports info ---
        ports_info_list = get_ports_info(host_info)

        print("==========================================\n")
        return os_info, ports_info_list

def get_os_namp(host_info):
    flag = 0
    # --- OS Detection NMAP ---
    os_matches = host_info.get('osmatch') or []
    os_info_list = [] # list of dicts, because can be multiple OS matches

    if os_matches:
        for match in os_matches:
            name = match.get('name') or "Unknown"
            accuracy = match.get('accuracy') or "Unknown"
            
            if int(accuracy) >= 90:
                os_classes = match.get('osclass') or []

                if os_classes:
                    os_family = os_classes[0].get("osfamily") or "Unknown"
                    os_gen = os_classes[0].get("osgen") or "Unknown"
                    vendor = os_classes[0].get('vendor') or "Unknown"
                else:
                    os_family = "Unknown"
                    os_gen = "Unknown"
                    vendor = "Unknown"
                
                print(f"OS Match: {name}, Vendor: {vendor}, Accuracy: {accuracy}%, Family: {os_family}")
                os_info_list.append({
                    "os_match": name,
                    "vendor": vendor,
                    "accuracy": accuracy,
                    "family": os_family,
                    "generation": os_gen
                })
            else: 
                print(f"OS Match found but low accuracy ({accuracy}%) : {name}")
                return None
        flag = 1
    elif flag == 0:
        pass

    if flag == 1:
        return os_info_list
    else:
        print("No OS match found")
        return None

def get_ports_info(host_info):
    ports_info_list = []
    for proto in host_info.all_protocols():
        print("Protocol: ", proto)

        ports = host_info[proto].keys()
        for port in ports:
            info = host_info[proto][port]
            state = info.get('state') or None
            name = info.get('name') or None
            product = info.get('product') or None
            version = info.get('version') or None
            extrainfo = info.get('extrainfo') or None

            # Combina informațiile despre serviciu/protocol într-un format structurat
            service_details = build_service_info(name, product, version, extrainfo)

            print(f"Port: {port}\t|State: {state}\t|Service: {name}\t|Product: {product}\t|Version: {version}\t|Extra Info: {extrainfo}")
            
            ports_info_list.append({
                "port": port,
                "protocol": proto,  # tcp/udp
                "state": state,
                "service": name or "unknown",  # Protocol/Service name
                "product": product,
                "version": version,
                "extrainfo": extrainfo,
                "service_full": service_details  # Informație completă combinată
            })

    return ports_info_list

def build_service_info(name, product, version, extrainfo):
    """Construiește informația completă despre serviciu/protocol"""
    if not name:
        return "Unknown service"
    
    service_info = name
    
    # Adaugă produsul dacă există
    if product:
        service_info += f" ({product}"
        
        # Adaugă versiunea dacă există
        if version:
            service_info += f" {version}"
        
        # Adaugă informații extra dacă există
        if extrainfo:
            service_info += f" - {extrainfo}"
            
        service_info += ")"
    elif version:
        # Dacă nu avem produs dar avem versiune
        service_info += f" (version {version})"
        if extrainfo:
            service_info += f" - {extrainfo}"
    elif extrainfo:
        # Dacă avem doar informații extra
        service_info += f" ({extrainfo})"
    
    return service_info

if __name__ == "__main__":
    get_device_info("192.168.32.231")
