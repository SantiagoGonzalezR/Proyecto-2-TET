from concurrent import futures
import grpc
import Service_pb2
import Service_pb2_grpc

HOST = "[::]:8080"


class MicroService(Service_pb2_grpc.MicroServiceServicer):
    def CheckOnline(self, response, context):
        return Service_pb2.Response(status=1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Service_pb2_grpc.add_MicroServiceServicer_to_server(MicroService(), server)
    server.add_insecure_port(HOST)
    print("Service is running... ")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
