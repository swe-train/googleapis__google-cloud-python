# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.cloud.videointelligence_v1p1beta1.proto import (
    video_intelligence_pb2 as google_dot_cloud_dot_videointelligence__v1p1beta1_dot_proto_dot_video__intelligence__pb2,
)
from google.longrunning import (
    operations_pb2 as google_dot_longrunning_dot_operations__pb2,
)


class VideoIntelligenceServiceStub(object):
    """Service that implements Google Cloud Video Intelligence API.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AnnotateVideo = channel.unary_unary(
            "/google.cloud.videointelligence.v1p1beta1.VideoIntelligenceService/AnnotateVideo",
            request_serializer=google_dot_cloud_dot_videointelligence__v1p1beta1_dot_proto_dot_video__intelligence__pb2.AnnotateVideoRequest.SerializeToString,
            response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
        )


class VideoIntelligenceServiceServicer(object):
    """Service that implements Google Cloud Video Intelligence API.
    """

    def AnnotateVideo(self, request, context):
        """Performs asynchronous video annotation. Progress and results can be
        retrieved through the `google.longrunning.Operations` interface.
        `Operation.metadata` contains `AnnotateVideoProgress` (progress).
        `Operation.response` contains `AnnotateVideoResponse` (results).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_VideoIntelligenceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "AnnotateVideo": grpc.unary_unary_rpc_method_handler(
            servicer.AnnotateVideo,
            request_deserializer=google_dot_cloud_dot_videointelligence__v1p1beta1_dot_proto_dot_video__intelligence__pb2.AnnotateVideoRequest.FromString,
            response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "google.cloud.videointelligence.v1p1beta1.VideoIntelligenceService",
        rpc_method_handlers,
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class VideoIntelligenceService(object):
    """Service that implements Google Cloud Video Intelligence API.
    """

    @staticmethod
    def AnnotateVideo(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.cloud.videointelligence.v1p1beta1.VideoIntelligenceService/AnnotateVideo",
            google_dot_cloud_dot_videointelligence__v1p1beta1_dot_proto_dot_video__intelligence__pb2.AnnotateVideoRequest.SerializeToString,
            google_dot_longrunning_dot_operations__pb2.Operation.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
