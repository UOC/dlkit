# Python 3.2+ only
from concurrent import futures

import time

import grpc

from dlkit.grpc_adapter.resource import BinLookupSessionServicer
from dlkit.proto import resource_pb2_grpc
from dlkit.runtime import PROXY_SESSION, RUNTIME
from dlkit.runtime.proxy_example import SimpleRequest

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


condition = PROXY_SESSION.get_proxy_condition()
dummy_request = SimpleRequest(username='grpc@test.com',
                              authenticated=True)
condition.set_http_request(dummy_request)

proxy = PROXY_SESSION.get_proxy(condition)
mgr = RUNTIME.get_service_manager('RESOURCE',
                                  proxy=proxy)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    resource_pb2_grpc.add_BinLookupSessionServicer_to_server(
        BinLookupSessionServicer(mgr._runtime), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
