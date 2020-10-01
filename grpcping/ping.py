# -*- coding: utf-8 -*-
import argparse
import os
import grpc
from concurrent import futures
from .pb.grpcpingpb_pb2 import SwapParams
from .pb.grpcpingpb_pb2 import Status as PbStatus
from .pb.grpcpingpb_pb2 import Params as PbParams
from .pb.grpcpingpb_pb2_grpc import gRpcPingServiceServicer, gRpcPingServiceStub, add_gRpcPingServiceServicer_to_server


class GrpcPingGw(gRpcPingServiceServicer):
    def Hello(self, request, context):
        print("-> receive HELLO from %s" % request.src)
        return PbStatus(status=200)

    def SwapImage(self, request_iter, context):
        sending = False
        i = 0
        for req in request_iter:
            if not sending:
                print("-> echo start")
                sending = True
            print(" --> echo: %d" % i)
            i += 1
            yield SwapParams(src=req.src, params=req.params)
        print("-> echo end")


class GrpcPing:
    def __init__(self, src_addr, image=None, grpc_size=1024*1024):
        self._src_addr = src_addr
        self._snd_filename = image
        self._grpc_size = grpc_size
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        add_gRpcPingServiceServicer_to_server(GrpcPingGw(), self._server)
        self._server.add_insecure_port('[::]:' + src_addr.split(':')[1])
        self._server.start()
        self._cnt = 0

    def __call__(self, dest):
        with grpc.insecure_channel(dest) as channel:
            try:
                req = PbParams(src=self._src_addr)
                stub = gRpcPingServiceStub(channel)
                response = stub.Hello(req)
                if response.status == 200:
                    print("Hello OK")

                    if self._snd_filename is not None:
                        with open('output' + os.path.splitext(self._snd_filename)[1], 'wb') as f_out:
                            swap_req_iter = self.SwapReqIter(self._snd_filename, self._src_addr, self._grpc_size)
                            for res in stub.SwapImage(swap_req_iter, timeout=10):
                                print(" resp: %d" % self._cnt)
                                self._cnt += 1
                                f_out.write(res.params)
                        print("file output OK!")

            except grpc.RpcError as e:
                print(e)

    def __del__(self):
        self._server.stop(0)

    class SwapReqIter(object):
        def __init__(self, file_name, src_addr, grpc_buf_size):
            self._src_addr = src_addr
            self._grpc_buf_size = grpc_buf_size
            self._f_in = open(file_name, mode='rb')
            self._f_in.seek(0)
            self._cnt = 0

        def __iter__(self):
            return self

        def __next__(self):
            read_buf = self._f_in.read(self._grpc_buf_size)
            if not read_buf:
                self._f_in.close()
                raise StopIteration()
            print(" read: %d" % self._cnt)
            self._cnt += 1
            return SwapParams(src=self._src_addr, params=read_buf)


def main():
    parser = argparse.ArgumentParser(description='grpcping')
    parser.add_argument('-s', '--src', required=True)
    parser.add_argument('-d', '--dst')
    parser.add_argument('-i', '--image')
    args = parser.parse_args()

    ping = GrpcPing(args.src, args.image)
    if args.dst is not None:
        ping(args.dst)
    else:
        while True:
            pass


if __name__ == "__main__":
    main()
