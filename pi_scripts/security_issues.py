def analyze_security_issues(device_data):
    """Analizează datele device-ului și identifică probleme de securitate"""
    issues = []
    
    ip = device_data.get('ip')
    ports = device_data.get('ports', [])
    os_info = device_data.get('os')
    
    # Verifică porturile deschise pentru probleme comune de securitate
    open_ports = []
    risky_ports = []
    critical_services = []
    
    for port_info in ports:
        if port_info.get('state') == 'open':
            port = port_info.get('port')
            service = port_info.get('service') or ''
            product = port_info.get('product') or ''
            
            # Safe lower() calls
            service = service.lower() if service else ''
            product = product.lower() if product else ''
            
            open_ports.append(port)
            
            # Detectează porturi riscante
            risky_port_issue = check_risky_ports(port, service, product)
            if risky_port_issue:
                risky_ports.append(risky_port_issue)
            
            # Detectează servicii critice
            critical_service_issue = check_critical_services(port, service, product)
            if critical_service_issue:
                critical_services.append(critical_service_issue)
    
    # Generează issues bazate pe analiză
    if open_ports:
        issues.append({
            "type": "open_ports",
            "severity": "medium", 
            "title": f"Open Ports Detected ({len(open_ports)} ports)",
            "description": f"Found {len(open_ports)} open ports on {ip}",
            "details": {
                "ports": open_ports,
                "recommendation": "Review if all open ports are necessary and properly secured"
            }
        })
    
    if risky_ports:
        issues.append({
            "type": "risky_ports",
            "severity": "high",
            "title": f"Risky Ports Detected ({len(risky_ports)} ports)",
            "description": f"Found potentially dangerous open ports on {ip}",
            "details": {
                "risky_ports": risky_ports,
                "recommendation": "Immediately review and secure or close these ports"
            }
        })
    
    if critical_services:
        issues.append({
            "type": "critical_services", 
            "severity": "critical",
            "title": f"Critical Services Exposed ({len(critical_services)} services)",
            "description": f"Found critical services exposed on {ip}",
            "details": {
                "services": critical_services,
                "recommendation": "Secure these services immediately or restrict access"
            }
        })
    
    # Verifică probleme specifice OS
    os_issues = check_os_issues(os_info)
    if os_issues:
        issues.extend(os_issues)
    
    return issues

def check_risky_ports(port, service, product):
    """Verifică dacă portul este considerat riscant"""
    risky_ports_db = {
        21: {"name": "FTP", "risk": "Unencrypted file transfer"},
        23: {"name": "Telnet", "risk": "Unencrypted remote access"},
        135: {"name": "RPC", "risk": "Windows RPC - potential for exploitation"},
        139: {"name": "NetBIOS", "risk": "File sharing vulnerabilities"},
        445: {"name": "SMB", "risk": "File sharing - check for SMB vulnerabilities"},
        1433: {"name": "MSSQL", "risk": "Database exposed to network"},
        3306: {"name": "MySQL", "risk": "Database exposed to network"},
        3389: {"name": "RDP", "risk": "Remote desktop - brute force target"},
        5432: {"name": "PostgreSQL", "risk": "Database exposed to network"},
        5900: {"name": "VNC", "risk": "Remote desktop - often weak authentication"},
        27017: {"name": "MongoDB", "risk": "Database often misconfigured"},
        6379: {"name": "Redis", "risk": "Database often without authentication"}
    }
    
    if port in risky_ports_db:
        return {
            "port": port,
            "service": service or risky_ports_db[port]["name"],
            "risk_level": "high",
            "risk_description": risky_ports_db[port]["risk"]
        }
    
    # Verifică servicii riscante bazate pe nume
    if service and any(risky in service for risky in ['ftp', 'telnet', 'rlogin', 'rsh']):
        return {
            "port": port,
            "service": service,
            "risk_level": "high", 
            "risk_description": "Unencrypted protocol detected"
        }
    
    return None

def check_critical_services(port, service, product):
    """Verifică servicii critice care necesită atenție specială"""
    critical_services_db = {
        22: {"name": "SSH", "check": "Ensure strong authentication"},
        80: {"name": "HTTP", "check": "Should use HTTPS instead"},
        443: {"name": "HTTPS", "check": "Verify certificate and configuration"},
        25: {"name": "SMTP", "check": "Check for open relay"},
        110: {"name": "POP3", "check": "Should use secure POP3S"},
        143: {"name": "IMAP", "check": "Should use secure IMAPS"},
        53: {"name": "DNS", "check": "Verify not open resolver"}
    }
    
    if port in critical_services_db:
        return {
            "port": port,
            "service": service or critical_services_db[port]["name"],
            "recommendation": critical_services_db[port]["check"]
        }
    
    return None

def check_os_issues(os_info):
    """Verifică probleme specifice sistemului de operare"""
    issues = []
    
    if not os_info or os_info == "Unknown":
        return issues
    
    # Pentru liste de OS-uri
    if isinstance(os_info, list):
        for os_match in os_info:
            os_name = os_match.get('os_match', '').lower()
            
            if 'windows' in os_name:
                if any(version in os_name for version in ['xp', '2003', 'vista', '2008']):
                    issues.append({
                        "type": "outdated_os",
                        "severity": "critical",
                        "title": "Outdated Windows Version",
                        "description": f"Running unsupported Windows version: {os_name}",
                        "details": {
                            "recommendation": "Upgrade to supported Windows version immediately"
                        }
                    })
    
    return issues

def generate_security_report(device_data):
    """Generează un raport complet de securitate pentru device"""
    issues = analyze_security_issues(device_data)
    
    # Calculează scorul de risc
    risk_score = calculate_risk_score(issues)
    
    return {
        "ip": device_data.get('ip'),
        "risk_score": risk_score,
        "total_issues": len(issues),
        "issues": issues,
        "summary": generate_summary(issues)
    }

def calculate_risk_score(issues):
    """Calculează scorul de risc (0-100)"""
    score = 0
    severity_weights = {
        "low": 10,
        "medium": 25, 
        "high": 50,
        "critical": 75
    }
    
    for issue in issues:
        severity = issue.get('severity', 'low')
        score += severity_weights.get(severity, 10)
    
    return min(score, 100)  # Cap la 100

def generate_summary(issues):
    """Generează un sumar al problemelor"""
    if not issues:
        return "No security issues detected"
    
    severity_count = {}
    for issue in issues:
        severity = issue.get('severity', 'low')
        severity_count[severity] = severity_count.get(severity, 0) + 1
    
    summary_parts = []
    for severity in ['critical', 'high', 'medium', 'low']:
        if severity in severity_count:
            count = severity_count[severity]
            summary_parts.append(f"{count} {severity}")
    
    return f"Found: {', '.join(summary_parts)} severity issues"
