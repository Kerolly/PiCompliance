from nmb.NetBIOS import NetBIOS
import socket



def get_hostname_mdns(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        print(f"Hostname: {hostname}")
    except:
        print("Could not get the hostname")
        return "Unknown"
    

    print("==========================================\n")

    return hostname


if __name__ == "__main__":
    windows_hostname("10.132.86.0-100")
    #get_hostname_mdns("10.132.86.0-100")