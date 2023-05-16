# importar los requerimientos del gRPC para conectar los monitores
from datetime import datetime
import time
import MicroService
import socket

# Conexion por gRPC
mc = MicroService()


def tiempoEjecucion(self):
    host="[::]:8080"
    address, port = host.split("]:")
    address = address.strip("[]")
    ipv4_address = socket.getaddrinfo(address, port, socket.AF_INET)[0][4][0]
    startTime = time.time()
    processCap = (time.time - startTime) / 2.5
    while True:
        mc(ipv4_address, processCap)
        processCap = (time.time - startTime) / 2.5

