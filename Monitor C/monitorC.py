# importar los requerimientos del gRPC para conectar los monitores
from datetime import datetime
import time
import MicroService

# Conexion por gRPC
mc = MicroService()


def tiempoEjecucion(self):
    startTime = time.time()
    processCap = (time.time - startTime) / 2.5
    while True:
        sendData(processCap)
        processCap = (time.time - startTime) / 2.5


def sendData(processCap):
    return "Enviar processCap por gRPC"
