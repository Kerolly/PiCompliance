import nmap
from save_json import save_to_json
import socket
from admin_privileges import ensure_elevated
import psutil

ensure_elevated()


def get_scanning_device_mac():
    try:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()

        local_mac = None
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address == local_ip:
                    
                    for mac_addr in addrs:
                        if mac_addr.family in (psutil.AF_LINK, getattr(socket, 'AF_PACKET', 17)):
                            local_mac = mac_addr.address
                            break
                    break
            if local_mac:
                break

        return local_ip, local_mac
    except Exception as e:
        print(f"Could not get IP/MAC: {e}")
        return None, None


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

    save_to_json(results, "nmap_ips_macs_scan.json")

    return results

if __name__ == "__main__":
    nmap_hosts_scan("192.168.27.0/24")
    #get_scanning_device_mac()