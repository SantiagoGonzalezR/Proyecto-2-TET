# importar los requerimientos del gRPC para conectar los monitores
from datetime import datetime
from concurrent import futures
import time, socket, grpc, Service_pb2, Service_pb2_grpc

HOST = "[::]:8080"


class MicroService(Service_pb2_grpc.MicroServiceServicer):
    startTime = 0

    def __init__(self):
        self.startTime = time.time()

    def CheckOnline(self, response, context):
        processCap = (time.time() - self.startTime) / 2.5
        return Service_pb2.Response(time=str(processCap))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Service_pb2_grpc.add_MicroServiceServicer_to_server(MicroService(), server)
    server.add_insecure_port(HOST)
    print("Service is running... ")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
