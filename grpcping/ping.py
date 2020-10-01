# -*- coding: utf-8 -*-
import argparse
import os
import grpc
from concurrent import futures
from .pb.grpcpingpb_pb2 import Status as PbStatus
from .pb.grpcpingpb_pb2 import Params as PbParams
from .pb.grpcpingpb_pb2_grpc import gRpcPingServiceServicer, gRpcPingServiceStub, add_gRpcPingServiceServicer_to_server


class GrpcPingGw(gRpcPingServiceServicer):
    def Hello(self, request, context):
        print(" -> receive HELLO from %s" % request.src)
        return PbStatus(status=200)


class GrpcPing:
    def __init__(self, self_port=8888):
        if os.name == 'posix':
            self._slf_addr = os.uname()[1] + ":" + str(self_port)
        else:
            self._slf_addr = "windows_os:" + str(self_port)
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        add_gRpcPingServiceServicer_to_server(GrpcPingGw(), self._server)
        self._server.add_insecure_port('[::]:' + str(self_port))
        self._server.start()

    def __call__(self, target):
        with grpc.insecure_channel(target) as channel:
            try:
                req = PbParams(src=self._slf_addr)
                stub = gRpcPingServiceStub(channel)
                response = stub.Hello(req)
                if response.status == 200:
                    print("Hello OK")
            except grpc.RpcError as e:
                print(e)

    def __del__(self):
        self._server.stop(0)


def main():
    parser = argparse.ArgumentParser(description='grpcping')
    parser.add_argument('-p', '--port', required=True)
    parser.add_argument('-t', '--target')
    args = parser.parse_args()

    ping = GrpcPing(args.port)
    if args.target is not None:
        ping(args.target)
    else:
        while True:
            pass


if __name__ == "__main__":
    main()
