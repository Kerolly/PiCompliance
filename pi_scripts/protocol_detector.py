import nmap
import socket

def detect_protocol_with_nmap(host, port):
    """Detecteaza protocolul folosind nmap cu service detection"""
    try:
        nm = nmap.PortScanner()
        # Foloseste -sV pentru service detection
        result = nm.scan(host, str(port), arguments='-sV --version-intensity 5')
        
        if host in result['scan'] and 'tcp' in result['scan'][host]:
            if port in result['scan'][host]['tcp']:
                service_info = result['scan'][host]['tcp'][port]
                
                # Extrage informatiile despre serviciu
                service_name = service_info.get('name', 'unknown')
                service_product = service_info.get('product', '')
                service_version = service_info.get('version', '')
                service_extrainfo = service_info.get('extrainfo', '')
                
                # Construieste informatia completa despre protocol
                protocol_info = service_name
                
                if service_product:
                    protocol_info += f" ({service_product}"
                    if service_version:
                        protocol_info += f" {service_version}"
                    if service_extrainfo:
                        protocol_info += f" - {service_extrainfo}"
                    protocol_info += ")"
                
                return protocol_info
                
    except Exception as e:
        print(f"Error detecting protocol for {host}:{port} - {e}")
        pass
    
    # Fallback la protocoale comune daca nmap nu merge
    return get_common_protocol(port)

def get_common_protocol(port):
    """Fallback pentru protocoale comune bazat pe port"""
    common_protocols = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        135: 'Microsoft RPC',
        139: 'NetBIOS',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'Microsoft SMB',
        993: 'IMAPS',
        995: 'POP3S',
        1433: 'Microsoft SQL Server',
        1521: 'Oracle',
        3306: 'MySQL',
        3389: 'Microsoft RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        8080: 'HTTP-Proxy',
        8443: 'HTTPS-Alt'
    }
    
    return common_protocols.get(port, 'Unknown')

def detect_protocol_banner_grab(host, port, timeout=3):
    """Detectare protocol prin banner grabbing ca backup"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        # Trimite cereri specifice pentru anumite porturi
        if port in [80, 8080]:
            sock.send(b'GET / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n')
        elif port == 21:
            pass  # FTP trimite banner automat
        elif port == 25:
            pass  # SMTP trimite banner automat
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        
        # Analizeaza banner-ul primit
        banner_upper = banner.upper()
        if 'SSH' in banner_upper:
            return f'SSH ({banner[:50]}...)'
        elif 'HTTP' in banner_upper:
            return f'HTTP ({banner[:50]}...)'
        elif 'FTP' in banner_upper:
            return f'FTP ({banner[:50]}...)'
        elif 'SMTP' in banner_upper:
            return f'SMTP ({banner[:50]}...)'
        elif banner:
            return f'Unknown ({banner[:30]}...)'
            
    except Exception:
        pass
    
    return get_common_protocol(port)
