from nmap_hosts_scan import nmap_hosts_scan
from get_hostname import get_hostname_mdns
from detailed_scan import get_device_info
from save_json import save_to_json
from admin_privileges import ensure_elevated
import socket
from vendor_scanner import get_vendor

ensure_elevated()

global scan_results
scan_results = []

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        print(f'Error:{e}')

import socket
import ipaddress

def get_cidr():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        
        net = ipaddress.IPv4Network(f"{ip}/24", strict=False)
        return str(net)
    except Exception:
        return None


def scan_network():
    ip_mac_list = nmap_hosts_scan(get_cidr())

    founded_devices = len(ip_mac_list)
    counter = 1

    number_of_devices = input(f"Enter number of devices to scan in detail (or press Enter to scan all)\nFounded: {founded_devices}: ")
    if number_of_devices.strip() == "":
        number_of_devices = founded_devices


    for device in ip_mac_list:
        if counter <= int(number_of_devices):
            # Try to get hostname
            hostname = get_hostname_mdns(device.get('ip'))
        
            #Try to get vendor
            vendor=get_vendor(device.get('mac'))
            
                
            # Try to get detailed info
            os_info, ports_info = get_device_info(device.get('ip'))
            
            scan_results.append({
                "ip": device.get('ip'),
                "mac": device.get('mac'),
                "vendor" : vendor,
                "hostname": hostname,
                "os": os_info,
                "ports": ports_info
            })
            counter += 1
        else:
            break
        
    print(f"=================== Done Scanning {number_of_devices} hosts =======================\n")
    
    print("--->Saving results to JSON file ...")
    save_to_json(scan_results, "scan_results.json")
    print("--->Results saved to: scan_results.json\n")
    

    return ip_mac_list

scan_network()