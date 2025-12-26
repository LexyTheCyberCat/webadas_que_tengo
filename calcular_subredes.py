#!/bin/python3
bits_ip = 32
print("calcular hosts utilizables por subred\n")

try:
    mascara = int(input("Ingrese la mascara: "))
    if mascara >= 31 and mascara <= 33:
        abc = bits_ip - mascara
        hosts = 2 ** abc
    else:
        abc = bits_ip - mascara
        saltos = 2 ** abc
        hosts = saltos - 2

    print(f"Hosts utilizables: {hosts}")
except ValueError:
    print("Ingrese un numero entero (Ej: 24)")
