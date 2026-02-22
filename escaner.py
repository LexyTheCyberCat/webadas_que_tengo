#!/usr/bin/python3

import socket
import argparse 

parse = argparse.ArgumentParser(description="Escáner de puertos TCP y UDP")
parse.add_argument("-ip", required=True, help="Host o dirección IP a escanear")
parse.add_argument("-p", "--port", type=int, required=False, help="Escanear puertoes específicos")
parse.add_argument("-u", "--udp", action="store_true", help="Escanear puertos UDP")
parse.add_argument("--open", action="store_true", help="Mostrar solo puertos abiertos")
args = parse.parse_args()

class colors:
    ROJO = '\033[91m'
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    RESET = '\033[0m'

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.settimeout(1)
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.settimeout(2)

ip = args.ip.strip()
puerto = None
resultado = None

TCP_PORT = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306]
UDP_PORT = [53, 67, 68, 69, 123, 161, 162, 500, 514, 520, 1900, 4500, 9999]

if any(c.isalpha() for c in ip):
    try:
        ip = socket.gethostbyname(ip)
        print(f"{colors.VERDE}[+]{colors.RESET} Dirección IP resuelta: {ip}")
    except socket.gaierror:
        print(f"{colors.ROJO}[-]{colors.RESET} Dominio no resuelto. Por favor, ingrese una IP válida o un nombre de dominio correcto.")
        exit(1)

def scan_port_tcp(ip, puerto):
    if args.port:
        puerto = args.port
        try:
            resultado = tcp.connect_ex((ip, puerto))
            if resultado == 0:
                print(f"{colors.VERDE}[+]{colors.RESET} Puerto {puerto} Abierto")
            else:
                print(f"{colors.ROJO}[-]{colors.RESET} Puerto {puerto} Cerrado")
        except socket.timeout: 
            print(f"{colors.AZUL}[*]{colors.RESET} Puerto {puerto} Abierto | Filtrado (Timeout)")
    else:
        for i in TCP_PORT:
            try:
                # Crear un socket nuevo para cada puerto
                tcp_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_temp.settimeout(0.5)
                resultado = tcp_temp.connect_ex((ip, i))
                if resultado == 0:
                    print(f"{colors.VERDE}[+]{colors.RESET} Puerto {i} Abierto")
                else:
                    print(f"{colors.ROJO}[-]{colors.RESET} Puerto {i} Cerrado")
                tcp_temp.close()
            except socket.timeout:
                print(f"{colors.AZUL}[*]{colors.RESET} Puerto {i} Abierto | Filtrado (Timeout)")
            except (ConnectionAbortedError):
                print(f"{colors.AZUL}[*]{colors.RESET} Puerto {i} Filtrado (Conexión abortada)")
            except (ConnectionRefusedError):
                print(f"{colors.ROJO}[-]{colors.RESET} Puerto {i} Cerrado")

def scan_port_udp(ip, puerto):
    if args.port:
        try:
            puerto = args.port
            udp.sendto(b'test', (ip, puerto))
            data, addr = udp.recvfrom(1024)
            if data:
                print(f"{colors.VERDE}[+]{colors.RESET} puerto {puerto} Abierto")
        except socket.timeout:
            print(f"{colors.ROJO}[-]{colors.RESET} puerto {puerto} Cerrado (Timeout)")
        except ConnectionRefusedError:
            print(f"{colors.ROJO}[-]{colors.RESET} puerto {puerto} Cerrado")
    elif args.udp:
        for i in UDP_PORT:
            udp_temp = None
            try:
                udp_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_temp.settimeout(2)
                udp_temp.sendto(b'test', (ip, i))
                data, addr = udp_temp.recvfrom(1024)
                if data:
                    print(f"{colors.VERDE}[+]{colors.RESET} puerto {i} Abierto")
            except socket.timeout:
                print(f"{colors.AZUL}[*]{colors.RESET} puerto {i} Abierto | Filtrado (Timeout)")
            except ConnectionRefusedError:
                print(f"{colors.ROJO}[-]{colors.RESET} puerto {i} Cerrado")
            finally:
                if udp_temp:
                    udp_temp.close()

if (puerto in TCP_PORT or puerto is None) and not args.udp:
    resultado = scan_port_tcp(ip, puerto)
    tcp.close()

elif (puerto in UDP_PORT or puerto is None) and args.udp:
     scan_port_udp(ip, puerto)
     udp.close()
