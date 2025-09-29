from nmap_hosts_scan import nmap_hosts_scan
from get_hostname import get_hostname_mdns, windows_hostname
from detailed_scan import get_device_info
from save_json import save_to_json
import socket

global scan_results
scan_results = []

def get_ip():
    my_ip = socket.gethostbyname(socket.getfqdn())
    cidr = '.'.join(my_ip.split('.')[:3]) + '.0/24'
    #print("CIDR Notation:", cidr)
    #print("IP Address:", my_ip)
    return cidr

def scan_network():
    ip_mac_list = nmap_hosts_scan(get_ip())

    founded_devices = len(ip_mac_list)
    counter = 1

    number_of_devices = input(f"Enter number of devices to scan in detail (or press Enter to scan all)\nFounded: {founded_devices}: ")
    if number_of_devices.strip() == "":
        number_of_devices = founded_devices


    for device in ip_mac_list:
        if counter <= int(number_of_devices):
            # Try to get hostname
            hostname = get_hostname_mdns(device.get('ip'))
            if hostname == "Unknown":
                hostname = windows_hostname(device.get('ip'))

            # Try to get detailed info
            os_info, ports_info = get_device_info(device.get('ip'))
            
            scan_results.append({
                "ip": device.get('ip'),
                "mac": device.get('mac'),
                "hostname": hostname,
                "os": os_info,
                "ports": ports_info
            })
            counter += 1
        else:
            break
        
    print(f"===================Done Scanning {number_of_devices} =======================\n")
    
    print("--->Saving results to JSON file ...")
    save_to_json(scan_results)
    print("--->Results saved to: scan_results.json\n")
    

    return ip_mac_list

scan_network()