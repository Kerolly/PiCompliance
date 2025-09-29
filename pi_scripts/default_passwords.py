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
]

def test_ssh_connection(ip, username, password, port=22):
    client = paramiko.SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=password,
                       timeout=5, banner_timeout=5, auth_timeout=5)
        print(f"[SUCCES] {ip}:{port} - {username}:{password}")
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

def scan_network_ssh(targets, port=22):
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
    datas = load_from_json('nmap_ips_scan.json') 
    ips = []
    for data in datas:
        temp = data.get('ip')
        ips.append(temp)
    print(ips)
    return ips
get_ips_from_json()    



targets = get_ips_from_json() 
scan_network_ssh(targets)



