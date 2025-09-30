import paramiko
import socket
from concurrent.futures import ThreadPoolExecutor
from save_json import load_from_json, save_to_json
from paramiko import SSHException, AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError

DEFAULT_CREDENTIALS = [
    {"username": "admin", "password": "admin"},
    {"username": "admin", "password": "password"},
    {"username": "admin", "password": "1234"},
    {"username": "admin", "password": "default"},
    {"username": "root", "password": "root"},
    {"username": "root", "password": "admin"},
    {"username": "user", "password": "user"},
    {"username": "user", "password": "password"},
    {"username": "admin", "password": ""},
    {"username": "administrator", "password": "password"},
    {"username": "pi", "password": "raspberry"},
    {"username": "ubuntu", "password": "ubuntu"},
    {"username": "cisco", "password": "cisco"},
]

def test_ssh_connection(ip, username, password, port=22):
    client = paramiko.SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=password,
                       timeout=5, banner_timeout=5, auth_timeout=5)
        print(f"[SUCCESS] {ip}:{port} - {username}:{password}")
        return True, False  # (login_ok, timed_out)
    except (socket.timeout, TimeoutError, NoValidConnectionsError) as e:
        print(f"[TIMEOUT] {ip}:{port} -> {e}")
        return False, True  # marchează timeout
    except AuthenticationException:
        print(f"[AUTH FAILED] {ip}:{port} - {username}:{password}")
        return False, False
    except SSHException as e:
        print(f"[SSH ERR] {ip}:{port} -> {e}")
        return False, False
    except Exception as e:
        print(f"[ERR] {ip}:{port} -> {e}")
        return False, False
    finally:
        try:
            client.close()
        except Exception:
            pass

def scan_device_ssh_credentials(ip, port=22):
    """Scanează un device pentru credențiale SSH default"""
    print(f"  --> Testing SSH default credentials for {ip}:{port}...")
    
    for idx, cred in enumerate(DEFAULT_CREDENTIALS):
        ok, timed_out = test_ssh_connection(ip, cred["username"], cred["password"], port=port)
        
        if timed_out:
            print(f"[SKIP HOST AFTER TIMEOUT] {ip}:{port}")
            return None  # Nu putem testa din cauza timeout
        
        if ok:
            return {
                "username": cred["username"],
                "password": cred["password"],
                "port": port,
                "status": "default_password_found"
            }
    
    return {"status": "no_default_credentials", "port": port}

def check_ssh_default_passwords(device_data):
    """Verifică dacă device-ul are SSH cu parolele default"""
    ip = device_data.get('ip')
    ports = device_data.get('ports', [])
    
    # Caută portul SSH în lista de porturi deschise
    ssh_ports = []
    for port_info in ports:
        if port_info.get('state') == 'open':
            port = port_info.get('port')
            service = port_info.get('service', '').lower()
            
            # Detectează SSH pe port 22 sau prin service name
            if port == 22 or service == 'ssh':
                ssh_ports.append(port)
    
    if not ssh_ports:
        return {"status": "no_ssh_service"}
    
    # Testează primul port SSH găsit
    ssh_port = ssh_ports[0]
    result = scan_device_ssh_credentials(ip, ssh_port)
    
    return result

def scan_network_ssh(targets, port=22):
    """Funcția originală pentru scanare batch"""
    for target in targets:
        print(f"Scanning {target}...")
        for idx, cred in enumerate(DEFAULT_CREDENTIALS):
            ok, timed_out = test_ssh_connection(target, cred["username"], cred["password"], port=port)
            
            if timed_out:
                print(f"[SKIP HOST AFTER TIMEOUT] {target}:{port}")
                break  # trece la următorul IP
            
            if ok:
                # opțional: dacă un login reușește, nu mai testa restul credențialelor
                break

def get_ips_from_json():
    """Funcția originală pentru extragere IP-uri"""
    datas = load_from_json('nmap_ips_scan.json') 
    ips = []
    for data in datas:
        temp = data.get('ip')
        ips.append(temp)
    print(ips)
    return ips

# Pentru testare independentă
if __name__ == "__main__":
    targets = get_ips_from_json() 
    scan_network_ssh(targets)
