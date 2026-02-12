#!/usr/bin/python3

import socket

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.settimeout(1)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.settimeout(1)

resultado = None
resultado_udp = None

ip = input("Ingrese la IP/Dominio: ").strip()
puerto = None

tcp_ranges = [(0, 1023), (1024, 49151), (49152, 65535)]
udp_ranges = [(0, 1023), (1024, 49151), (49152, 65535)] 

if any(c.isalpha() for c in ip):
    try:
        ip = socket.gethostbyname(ip)
        print(f"Dirección IP resuelta: {ip}")
    except socket.gaierror:
        print("Dominio no resuelto. Por favor, ingrese una IP válida o un nombre de dominio correcto.")
        exit(1)

def scan_port_tcp(ip, puerto):
    try:
        resultado = tcp.connect_ex((ip, puerto))
        return resultado

    except socket.error as e:
        print("Error al conectar: {}".format(e))
        exit(1)

def scan_port_udp(ip, puerto):
    try:
        udp.sendto(b'', (ip, puerto))
        resultado_udp = udp.recvfrom(1024)
        return None

    except socket.timeout:
        resultado_udp = 1
        return resultado_udp

    except ConnectionRefusedError:
        resultado_udp = 2
        return resultado_udp

try:   
    puerto = int(input("Ingrese el puerto: ").strip())
    if puerto < 0 or puerto > 65535:
        raise ValueError()

except ValueError:
    print("Por favor, ingrese un número válido para el puerto.")
    exit(1)

if any(inicio <= puerto <= fin for inicio, fin in tcp_ranges):
    resultado = scan_port_tcp(ip, puerto)
    tcp.close()
    
    if resultado == 0:
        print(f"[+] Puerto {puerto} Abierto") 
    
    else:
        print(f"[-] Puerto {puerto} Cerrado")

elif any(inicio <= puerto <= fin for inicio, fin in udp_ranges):
     scan_port_udp(ip, puerto)
     udp.close()
     
     if resultado_udp is None:
        print(f"[+] Puerto {puerto} Abierto")
     
     elif resultado_udp == 1:
        print(f"[-] Puerto {puerto} Abierto | Filtrado")
     
     else:
        print(f"[-] Puerto {puerto} Cerrado")                          