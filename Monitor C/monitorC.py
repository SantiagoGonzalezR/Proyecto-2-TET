# importar los requerimientos del gRPC para conectar los monitores
from datetime import datetime
from concurrent import futures
import time, socket, grpc, Service_pb2, Service_pb2_grpc

HOST = "[::]:8080"


class MicroService(Service_pb2_grpc.MicroServiceServicer):
    
    def CheckOnline(self, response, context):
        host = "[::]:8080"
        address, port = host.split("]:")
        address = address.strip("[]")
        ipv4_address = socket.getaddrinfo(address, port, socket.AF_INET)[0][4][0]
        startTime = time.time()
        processCap = (time.time - startTime) / 2.5
        while True:
            processCap = (time.time - startTime) / 2.5
        return Service_pb2.Response(status=1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Service_pb2_grpc.add_MicroServiceServicer_to_server(MicroService(), server)
    server.add_insecure_port(HOST)
    print("Service is running... ")
    server.start()
    server.wait_for_termination()


def tiempoEjecucion(self):
    host = "[::]:8080"
    address, port = host.split("]:")
    address = address.strip("[]")
    ipv4_address = socket.getaddrinfo(address, port, socket.AF_INET)[0][4][0]
    startTime = time.time()
    processCap = (time.time - startTime) / 2.5
    while True:
        MicroService.CheckOnline(ipv4_address, processCap)
        processCap = (time.time - startTime) / 2.5


if __name__ == "__main__":
    serve()
