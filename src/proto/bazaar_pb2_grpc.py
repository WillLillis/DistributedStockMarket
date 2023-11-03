# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import bazaar_pb2 as bazaar__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class BazaarStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Lookup = channel.unary_unary(
                '/Bazaar/Lookup',
                request_serializer=bazaar__pb2.LookupRequest.SerializeToString,
                response_deserializer=bazaar__pb2.LookupResponse.FromString,
                )
        self.Order = channel.unary_unary(
                '/Bazaar/Order',
                request_serializer=bazaar__pb2.OrderRequest.SerializeToString,
                response_deserializer=bazaar__pb2.OrderResponse.FromString,
                )
        self.Update = channel.unary_unary(
                '/Bazaar/Update',
                request_serializer=bazaar__pb2.UpdateRequest.SerializeToString,
                response_deserializer=bazaar__pb2.UpdateResponse.FromString,
                )
        self.GetOrder = channel.unary_unary(
                '/Bazaar/GetOrder',
                request_serializer=bazaar__pb2.GetOrderRequest.SerializeToString,
                response_deserializer=bazaar__pb2.GetOrderResponse.FromString,
                )
        self.HealthCheck = channel.unary_unary(
                '/Bazaar/HealthCheck',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=bazaar__pb2.HealthCheckResponse.FromString,
                )
        self.SignalOrderLeader = channel.unary_unary(
                '/Bazaar/SignalOrderLeader',
                request_serializer=bazaar__pb2.SignalOrderLeaderRequest.SerializeToString,
                response_deserializer=bazaar__pb2.SignalOrderLeaderResponse.FromString,
                )
        self.FollowerUpdate = channel.unary_unary(
                '/Bazaar/FollowerUpdate',
                request_serializer=bazaar__pb2.FollowerUpdateRequest.SerializeToString,
                response_deserializer=bazaar__pb2.FollowerUpdateResponse.FromString,
                )
        self.OrderLogRecover = channel.unary_unary(
                '/Bazaar/OrderLogRecover',
                request_serializer=bazaar__pb2.OrderLogRecoverRequest.SerializeToString,
                response_deserializer=bazaar__pb2.OrderLogRecoverResponse.FromString,
                )


class BazaarServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Lookup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Order(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HealthCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SignalOrderLeader(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FollowerUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OrderLogRecover(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BazaarServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Lookup': grpc.unary_unary_rpc_method_handler(
                    servicer.Lookup,
                    request_deserializer=bazaar__pb2.LookupRequest.FromString,
                    response_serializer=bazaar__pb2.LookupResponse.SerializeToString,
            ),
            'Order': grpc.unary_unary_rpc_method_handler(
                    servicer.Order,
                    request_deserializer=bazaar__pb2.OrderRequest.FromString,
                    response_serializer=bazaar__pb2.OrderResponse.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=bazaar__pb2.UpdateRequest.FromString,
                    response_serializer=bazaar__pb2.UpdateResponse.SerializeToString,
            ),
            'GetOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrder,
                    request_deserializer=bazaar__pb2.GetOrderRequest.FromString,
                    response_serializer=bazaar__pb2.GetOrderResponse.SerializeToString,
            ),
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=bazaar__pb2.HealthCheckResponse.SerializeToString,
            ),
            'SignalOrderLeader': grpc.unary_unary_rpc_method_handler(
                    servicer.SignalOrderLeader,
                    request_deserializer=bazaar__pb2.SignalOrderLeaderRequest.FromString,
                    response_serializer=bazaar__pb2.SignalOrderLeaderResponse.SerializeToString,
            ),
            'FollowerUpdate': grpc.unary_unary_rpc_method_handler(
                    servicer.FollowerUpdate,
                    request_deserializer=bazaar__pb2.FollowerUpdateRequest.FromString,
                    response_serializer=bazaar__pb2.FollowerUpdateResponse.SerializeToString,
            ),
            'OrderLogRecover': grpc.unary_unary_rpc_method_handler(
                    servicer.OrderLogRecover,
                    request_deserializer=bazaar__pb2.OrderLogRecoverRequest.FromString,
                    response_serializer=bazaar__pb2.OrderLogRecoverResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Bazaar', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Bazaar(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Lookup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bazaar/Lookup',
            bazaar__pb2.LookupRequest.SerializeToString,
            bazaar__pb2.LookupResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Order(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bazaar/Order',
            bazaar__pb2.OrderRequest.SerializeToString,
            bazaar__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bazaar/Update',
            bazaar__pb2.UpdateRequest.SerializeToString,
            bazaar__pb2.UpdateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bazaar/GetOrder',
            bazaar__pb2.GetOrderRequest.SerializeToString,
            bazaar__pb2.GetOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def HealthCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bazaar/HealthCheck',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            bazaar__pb2.HealthCheckResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SignalOrderLeader(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bazaar/SignalOrderLeader',
            bazaar__pb2.SignalOrderLeaderRequest.SerializeToString,
            bazaar__pb2.SignalOrderLeaderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FollowerUpdate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bazaar/FollowerUpdate',
            bazaar__pb2.FollowerUpdateRequest.SerializeToString,
            bazaar__pb2.FollowerUpdateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def OrderLogRecover(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bazaar/OrderLogRecover',
            bazaar__pb2.OrderLogRecoverRequest.SerializeToString,
            bazaar__pb2.OrderLogRecoverResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)