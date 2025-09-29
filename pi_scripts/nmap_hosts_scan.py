import nmap
from save_json import save_to_json

from admin_privileges import ensure_elevated

ensure_elevated()


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

    results = []
    for host in hosts:
        #print(scanner[host]['addresses'])
        #print(scanner[host]['hostnames'])
        #results[host] = scanner[host]['hostnames']

        results.append ({
            "ip": scanner[host]['addresses'].get('ipv4') or "Unknown",
             "mac": scanner[host]['addresses'].get('mac') if 'mac' in scanner[host]['addresses'] else "Not available"
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