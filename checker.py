#!/usr/bin/env python3
"""
Network Health Checker
-----------------------
Programa que revisa si varios hosts (IPs o dominios) estan activos,
y si tienen ciertos puertos abiertos. Al final genera un reporte en
pantalla y otro en un archivo CSV.

Brayan Vargas Madrigal
"""

import csv
import platform
import socket
import subprocess
from datetime import datetime

# Archivo donde estan los hosts a revisar
ARCHIVO_HOSTS = "hosts.txt"

# Archivo donde se va a guardar el reporte
ARCHIVO_REPORTE = "report.csv"

# Puertos que vamos a revisar en cada host
PUERTOS = [22, 80, 443, 3389]


def leer_hosts(archivo):
    """Lee el archivo de hosts y devuelve una lista con cada host."""
    hosts = []

    try:
        f = open(archivo, "r", encoding="utf-8")
    except FileNotFoundError:
        print("No se encontro el archivo:", archivo)
        return hosts

    for linea in f:
        linea = linea.strip()  # quitar espacios y saltos de linea
        # ignorar lineas vacias y comentarios
        if linea == "" or linea.startswith("#"):
            continue
        hosts.append(linea)

    f.close()
    return hosts


def hacer_ping(host):
    """Hace ping a un host y devuelve True si respondio, False si no."""
    sistema = platform.system().lower()

    if sistema == "windows":
        comando = ["ping", "-n", "1", "-w", "2000", host]
    else:
        comando = ["ping", "-c", "1", "-W", "2", host]

    try:
        resultado = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if resultado.returncode == 0:
            return True
        else:
            return False
    except Exception:
        return False


def revisar_puerto(host, puerto):
    """Intenta conectarse a un puerto especifico del host. True si abre."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((host, puerto))
        s.close()
        return True
    except Exception:
        return False


def revisar_host(host):
    """Revisa un host: hace ping y revisa cada puerto de la lista PUERTOS."""
    responde_ping = hacer_ping(host)

    estado_puertos = {}
    for puerto in PUERTOS:
        estado_puertos[puerto] = revisar_puerto(host, puerto)

    # el host se considera activo si responde al ping
    # o si al menos un puerto esta abierto
    activo = responde_ping
    for puerto in estado_puertos:
        if estado_puertos[puerto]:
            activo = True

    return {
        "host": host,
        "activo": activo,
        "puertos": estado_puertos,
    }


def mostrar_reporte(resultados):
    """Muestra el reporte en pantalla en forma de tabla simple."""
    encabezado = "Host".ljust(18) + "Status".ljust(10)
    for puerto in PUERTOS:
        encabezado += str(puerto).ljust(6)

    print(encabezado)
    print("-" * len(encabezado))

    for r in resultados:
        if r["activo"]:
            estado = "UP"
        else:
            estado = "DOWN"

        linea = r["host"].ljust(18) + estado.ljust(10)

        if r["activo"]:
            for puerto in PUERTOS:
                if r["puertos"][puerto]:
                    linea += "OK".ljust(6)
                else:
                    linea += "X".ljust(6)

        print(linea)


def guardar_csv(resultados, archivo):
    """Guarda el reporte en un archivo CSV."""
    f = open(archivo, "w", newline="", encoding="utf-8")
    escritor = csv.writer(f)

    # armar encabezado
    encabezado = ["host", "status"]
    for puerto in PUERTOS:
        encabezado.append("puerto_" + str(puerto))
    encabezado.append("fecha")
    escritor.writerow(encabezado)

    fecha_actual = datetime.now().isoformat(timespec="seconds")

    for r in resultados:
        if r["activo"]:
            estado = "UP"
        else:
            estado = "DOWN"

        fila = [r["host"], estado]

        for puerto in PUERTOS:
            if not r["activo"]:
                fila.append("")
            elif r["puertos"][puerto]:
                fila.append("OK")
            else:
                fila.append("CLOSED")

        fila.append(fecha_actual)
        escritor.writerow(fila)

    f.close()


def main():
    hosts = leer_hosts(ARCHIVO_HOSTS)

    if len(hosts) == 0:
        print("No hay hosts para revisar.")
        return

    print("Revisando", len(hosts), "host(s)...")
    print()

    resultados = []
    for host in hosts:
        resultado = revisar_host(host)
        resultados.append(resultado)

    mostrar_reporte(resultados)
    guardar_csv(resultados, ARCHIVO_REPORTE)

    print()
    print("Reporte guardado en:", ARCHIVO_REPORTE)


if __name__ == "__main__":
    main()