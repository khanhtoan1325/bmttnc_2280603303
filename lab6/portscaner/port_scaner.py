import socket

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389]

def scan_common_ports(domain):
    open_ports = []
    try:
        ip = socket.gethostbyname(domain)
        print(f"Scanning IP: {ip}")
    except socket.gaierror:
        print("Không thể phân giải tên miền.")
        return open_ports

    for port in COMMON_PORTS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            s.close()
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

    return open_ports

def main():
    domain = input("Enter the target domain: ")
    open_ports = scan_common_ports(domain)

    if open_ports:
        print("Open common ports:")
        for port in open_ports:
            print(f"Port {port} is open")
    else:
        print("No open common ports found.")

if __name__ == '__main__':
    main()
