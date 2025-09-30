from nmap_hosts_scan import nmap_hosts_scan
from get_hostname import get_hostname_mdns
from detailed_scan import get_device_info
from save_json import save_to_json, json_to_pdf
from admin_privileges import ensure_elevated
from security_issues import generate_security_report
from default_passwords import check_ssh_default_passwords
import socket
import ipaddress
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
        return ip
    except Exception as e:
        print(f'Error:{e}')

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
            print(f"\n=== Scanning device {counter}/{number_of_devices}: {device.get('ip')} ===")
            
            # Try to get hostname
            hostname = get_hostname_mdns(device.get('ip'))
        
            # Try to get vendor
            vendor = get_vendor(device.get('mac'))
                
            # Try to get detailed info
            os_info, ports_info = get_device_info(device.get('ip'))
            
            # Creează datele device-ului
            device_data = {
                "ip": device.get('ip'),
                "mac": device.get('mac'),
                "vendor": vendor,
                "hostname": hostname,
                "os": os_info,
                "ports": ports_info
            }
            
            # Verifică parolele SSH default
            print(f"---> Checking SSH default passwords for {device.get('ip')}...")
            ssh_creds_result = check_ssh_default_passwords(device_data)
            
            # Determină statusul parolelor
            if ssh_creds_result.get('status') == 'default_password_found':
                password_status = {
                    "status": "default_password_unsafe", 
                    "details": {
                        "username": ssh_creds_result.get('username'),
                        "password": ssh_creds_result.get('password'),
                        "port": ssh_creds_result.get('port')
                    },
                    "recommendation": "CRITICAL: Change SSH password immediately!"
                }
                print(f"  ⚠️  CRITICAL: Default SSH credentials found! {ssh_creds_result.get('username')}:{ssh_creds_result.get('password')}")
            elif ssh_creds_result.get('status') == 'no_default_credentials':
                password_status = {
                    "status": "password_safe",
                    "details": "No default SSH credentials found",
                    "recommendation": "SSH appears to have secure credentials"
                }
                print(f"  ✅ SSH credentials appear secure")
            elif ssh_creds_result.get('status') == 'no_ssh_service':
                password_status = {
                    "status": "password_safe", 
                    "details": "No SSH service detected - No remote access vulnerability",
                    "recommendation": "✅ SECURE: Device has no SSH service exposed"
                }
                print(f"  ✅ Password Safe - No SSH service running")
            else:
                password_status = {
                    "status": "unknown",
                    "details": "Could not test SSH credentials (timeout or error)",
                    "recommendation": "Manual verification recommended"
                }
                print(f"  ❓ Could not test SSH credentials")
            
            # Adaugă statusul parolelor la device data
            device_data["password_security"] = password_status
            
            # Generează raportul de securitate (din security_issues.py)
            print(f"---> Analyzing security issues for {device.get('ip')}...")
            security_report = generate_security_report(device_data)
            device_data["security_analysis"] = security_report
            
            # Afișează sumar securitate
            risk_score = security_report["risk_score"]
            total_issues = security_report["total_issues"]
            password_risk = "HIGH RISK" if password_status["status"] == "default_password_unsafe" else "SAFE"
            
            print(f"Security Risk Score: {risk_score}/100 | Issues: {total_issues} | Password Security: {password_risk}")
            print(f"Summary: {security_report['summary']}")
            
            scan_results.append(device_data)
            counter += 1
        else:
            break
        
    print(f"\n=================== Done Scanning {number_of_devices} hosts =======================\n")
    
    print("--->Saving results to JSON file ...")
    save_to_json(scan_results, "scan_results.json")
    print("--->Results saved to: scan_results.json\n")

    #print("--->Generating PDF report ...")
    #json_to_pdf("scan_results.json", "scan_report.pdf")
    #print("--> Results saved to: scan_report.pdf\n")

    
    # Afișează sumar general de securitate
    print_security_summary(scan_results)
    
    return ip_mac_list

def print_security_summary(results):
    """Afișează un sumar general al problemelor de securitate"""
    print("\n" + "="*60)
    print("NETWORK SECURITY SUMMARY")
    print("="*60)
    
    high_risk_devices = []
    default_password_devices = []
    total_issues = 0
    
    for device in results:
        security = device.get('security_analysis', {})
        password_sec = device.get('password_security', {})
        
        risk_score = security.get('risk_score', 0)
        issues_count = security.get('total_issues', 0)
        total_issues += issues_count
        
        # Verifică parolele default
        if password_sec.get('status') == 'default_password_unsafe':
            default_password_devices.append({
                'ip': device.get('ip'),
                'hostname': device.get('hostname'),
                'username': password_sec.get('details', {}).get('username'),
                'password': password_sec.get('details', {}).get('password')
            })
        
        if risk_score >= 50 or password_sec.get('status') == 'default_password_unsafe':
            high_risk_devices.append({
                'ip': device.get('ip'),
                'hostname': device.get('hostname'),
                'risk_score': risk_score,
                'issues': issues_count,
                'has_default_password': password_sec.get('status') == 'default_password_unsafe'
            })
    
    print(f"Total devices scanned: {len(results)}")
    print(f"Total security issues found: {total_issues}")
    print(f"Devices with default passwords: {len(default_password_devices)}")
    print(f"High-risk devices: {len(high_risk_devices)}")
    
    if default_password_devices:
        print("\n🚨 CRITICAL - DEVICES WITH DEFAULT PASSWORDS:")
        print("-" * 50)
        for device in default_password_devices:
            hostname = device['hostname'] if device['hostname'] else 'Unknown'
            print(f"• {device['ip']} ({hostname}) - SSH: {device['username']}:{device['password']}")
    
    if high_risk_devices:
        print("\nHIGH-RISK DEVICES:")
        print("-" * 40)
        for device in high_risk_devices:
            hostname = device['hostname'] if device['hostname'] else 'Unknown'
            risk_indicator = " 🚨 DEFAULT PASSWORD!" if device['has_default_password'] else ""
            print(f"• {device['ip']} ({hostname}) - Risk: {device['risk_score']}/100 - Issues: {device['issues']}{risk_indicator}")
    
    print("\n" + "="*60)

scan_network()
