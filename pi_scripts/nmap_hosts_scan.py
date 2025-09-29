import nmap
from save_json import save_to_json
import socket
from admin_privileges import ensure_elevated
import psutil

ensure_elevated()


def get_scanning_device_mac():
    try:
        my_hostname = socket.gethostname()
        local_ip = socket.gethostbyname(my_hostname)
        print(f"My hostname: {my_hostname}")
        print(f"My IP address: {local_ip}")

        local_mac = None

        for iface, addrs in psutil.net_if_addrs().items():
            # Check if this interface has the local IP
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address == local_ip:
                    # Found the interface with the local IP, now get its MAC address
                    for mac_addr in addrs:
                        if mac_addr.family in (psutil.AF_LINK, getattr(socket, 'AF_PACKET', 17)):
                            local_mac = mac_addr.address
                            break
                    break
            if local_mac:
                break
                
        print(f"My MAC address: {local_mac}")
        return local_ip, local_mac
    
    except Exception as e:
        print(f"Could not get the mac address: {e}")
        return "Unknown"


def nmap_hosts_scan(ip_range):

    scanner = nmap.PortScanner()
    options = "-sn -PR"  # Ping scan
    """
    -sn: Ping scan
    -PR: ARP ping
    -R:  reverse DNS
    """
    print("---> Starting scanning network...")
    print("...")
    print("...")

    scanner.scan(hosts=ip_range, arguments=options)

    hosts = scanner.all_hosts()
    local_ip, local_mac = get_scanning_device_mac()

    results = []
    for host in hosts:
        #print(scanner[host]['addresses'])
        #print(scanner[host]['hostnames'])
        #results[host] = scanner[host]['hostnames']

        if scanner[host]['addresses'].get('ipv4') == local_ip:
            mac = local_mac
        else:
            mac = scanner[host]['addresses'].get('mac') or "Not available"

        ip = scanner[host]['addresses'].get('ipv4') or "Unknown"

        results.append ({
            "ip": ip,
             "mac": mac
        })

    print("--->Scan complete")
    print(f"--->Found {len(results)} hosts\n")

    print("--->Devices:")
    for result in results:
        print(f"IP: {result['ip']}, MAC: {result['mac']}")

    print("==========================================\n")

    save_to_json(results, "nmap_ips_scan.json")

    return results

if __name__ == "__main__":
    nmap_hosts_scan("192.168.27.0/24")
    #get_scanning_device_mac()