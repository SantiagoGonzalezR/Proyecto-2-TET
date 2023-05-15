# importar los requerimientos del gRPC para conectar los monitores
from datetime import datetime
import time
import MicroService

# Conexion por gRPC
mc = MicroService()


def tiempoEjecucion(self):
    host="[::]:8080"
    startTime = time.time()
    processCap = (time.time - startTime) / 2.5
    while True:
        mc(host, processCap)
        processCap = (time.time - startTime) / 2.5

