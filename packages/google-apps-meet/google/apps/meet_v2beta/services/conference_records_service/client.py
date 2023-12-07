# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import os
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.apps.meet_v2beta import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import timestamp_pb2  # type: ignore

from google.apps.meet_v2beta.services.conference_records_service import pagers
from google.apps.meet_v2beta.types import resource, service

from .transports.base import DEFAULT_CLIENT_INFO, ConferenceRecordsServiceTransport
from .transports.grpc import ConferenceRecordsServiceGrpcTransport
from .transports.grpc_asyncio import ConferenceRecordsServiceGrpcAsyncIOTransport
from .transports.rest import ConferenceRecordsServiceRestTransport


class ConferenceRecordsServiceClientMeta(type):
    """Metaclass for the ConferenceRecordsService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ConferenceRecordsServiceTransport]]
    _transport_registry["grpc"] = ConferenceRecordsServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = ConferenceRecordsServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = ConferenceRecordsServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[ConferenceRecordsServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class ConferenceRecordsServiceClient(metaclass=ConferenceRecordsServiceClientMeta):
    """REST API for services dealing with conference records."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "meet.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ConferenceRecordsServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ConferenceRecordsServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ConferenceRecordsServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ConferenceRecordsServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def conference_record_path(
        conference_record: str,
    ) -> str:
        """Returns a fully-qualified conference_record string."""
        return "conferenceRecords/{conference_record}".format(
            conference_record=conference_record,
        )

    @staticmethod
    def parse_conference_record_path(path: str) -> Dict[str, str]:
        """Parses a conference_record path into its component segments."""
        m = re.match(r"^conferenceRecords/(?P<conference_record>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def participant_path(
        conference_record: str,
        participant: str,
    ) -> str:
        """Returns a fully-qualified participant string."""
        return (
            "conferenceRecords/{conference_record}/participants/{participant}".format(
                conference_record=conference_record,
                participant=participant,
            )
        )

    @staticmethod
    def parse_participant_path(path: str) -> Dict[str, str]:
        """Parses a participant path into its component segments."""
        m = re.match(
            r"^conferenceRecords/(?P<conference_record>.+?)/participants/(?P<participant>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def participant_session_path(
        conference_record: str,
        participant: str,
        participant_session: str,
    ) -> str:
        """Returns a fully-qualified participant_session string."""
        return "conferenceRecords/{conference_record}/participants/{participant}/participantSessions/{participant_session}".format(
            conference_record=conference_record,
            participant=participant,
            participant_session=participant_session,
        )

    @staticmethod
    def parse_participant_session_path(path: str) -> Dict[str, str]:
        """Parses a participant_session path into its component segments."""
        m = re.match(
            r"^conferenceRecords/(?P<conference_record>.+?)/participants/(?P<participant>.+?)/participantSessions/(?P<participant_session>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def recording_path(
        conference_record: str,
        recording: str,
    ) -> str:
        """Returns a fully-qualified recording string."""
        return "conferenceRecords/{conference_record}/recordings/{recording}".format(
            conference_record=conference_record,
            recording=recording,
        )

    @staticmethod
    def parse_recording_path(path: str) -> Dict[str, str]:
        """Parses a recording path into its component segments."""
        m = re.match(
            r"^conferenceRecords/(?P<conference_record>.+?)/recordings/(?P<recording>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def space_path(
        space: str,
    ) -> str:
        """Returns a fully-qualified space string."""
        return "spaces/{space}".format(
            space=space,
        )

    @staticmethod
    def parse_space_path(path: str) -> Dict[str, str]:
        """Parses a space path into its component segments."""
        m = re.match(r"^spaces/(?P<space>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def transcript_path(
        conference_record: str,
        transcript: str,
    ) -> str:
        """Returns a fully-qualified transcript string."""
        return "conferenceRecords/{conference_record}/transcripts/{transcript}".format(
            conference_record=conference_record,
            transcript=transcript,
        )

    @staticmethod
    def parse_transcript_path(path: str) -> Dict[str, str]:
        """Parses a transcript path into its component segments."""
        m = re.match(
            r"^conferenceRecords/(?P<conference_record>.+?)/transcripts/(?P<transcript>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def transcript_entry_path(
        conference_record: str,
        transcript: str,
        entry: str,
    ) -> str:
        """Returns a fully-qualified transcript_entry string."""
        return "conferenceRecords/{conference_record}/transcripts/{transcript}/entries/{entry}".format(
            conference_record=conference_record,
            transcript=transcript,
            entry=entry,
        )

    @staticmethod
    def parse_transcript_entry_path(path: str) -> Dict[str, str]:
        """Parses a transcript_entry path into its component segments."""
        m = re.match(
            r"^conferenceRecords/(?P<conference_record>.+?)/transcripts/(?P<transcript>.+?)/entries/(?P<entry>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, ConferenceRecordsServiceTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the conference records service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ConferenceRecordsServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        client_options = cast(client_options_lib.ClientOptions, client_options)

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ConferenceRecordsServiceTransport):
            # transport is a ConferenceRecordsServiceTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def get_conference_record(
        self,
        request: Optional[Union[service.GetConferenceRecordRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resource.ConferenceRecord:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a conference record by conference ID.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_get_conference_record():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.GetConferenceRecordRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_conference_record(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.GetConferenceRecordRequest, dict]):
                The request object. Request to get a conference record.
            name (str):
                Required. Resource name of the
                conference.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.types.ConferenceRecord:
                [Developer Preview](\ https://developers.google.com/workspace/preview).
                   Single instance of a meeting held in a space.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.GetConferenceRecordRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetConferenceRecordRequest):
            request = service.GetConferenceRecordRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_conference_record]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_conference_records(
        self,
        request: Optional[Union[service.ListConferenceRecordsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConferenceRecordsPager:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the conference records by start time and in descending
        order.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_list_conference_records():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.ListConferenceRecordsRequest(
                )

                # Make the request
                page_result = client.list_conference_records(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.ListConferenceRecordsRequest, dict]):
                The request object. Request to fetch list of conference
                records per user.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.services.conference_records_service.pagers.ListConferenceRecordsPager:
                Response of ListConferenceRecords
                method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListConferenceRecordsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListConferenceRecordsRequest):
            request = service.ListConferenceRecordsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_conference_records]

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListConferenceRecordsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_participant(
        self,
        request: Optional[Union[service.GetParticipantRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resource.Participant:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a participant by participant ID.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_get_participant():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.GetParticipantRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_participant(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.GetParticipantRequest, dict]):
                The request object. Request to get a Participant.
            name (str):
                Required. Resource name of the
                participant.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.types.Participant:
                [Developer Preview](\ https://developers.google.com/workspace/preview).
                   User who attended or is attending a conference.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.GetParticipantRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetParticipantRequest):
            request = service.GetParticipantRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_participant]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_participants(
        self,
        request: Optional[Union[service.ListParticipantsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListParticipantsPager:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the participants in a conference record, by default
        ordered by join time and in descending order. This API supports
        ``fields`` as standard parameters like every other API. However,
        when the ``fields`` request parameter is omitted, this API
        defaults to ``'participants/*, next_page_token'``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_list_participants():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.ListParticipantsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_participants(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.ListParticipantsRequest, dict]):
                The request object. Request to fetch list of participant
                per conference.
            parent (str):
                Required. Format:
                ``conferenceRecords/{conference_record}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.services.conference_records_service.pagers.ListParticipantsPager:
                Response of ListParticipants method.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListParticipantsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListParticipantsRequest):
            request = service.ListParticipantsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_participants]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListParticipantsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_participant_session(
        self,
        request: Optional[Union[service.GetParticipantSessionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resource.ParticipantSession:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a participant session by participant session ID.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_get_participant_session():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.GetParticipantSessionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_participant_session(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.GetParticipantSessionRequest, dict]):
                The request object. Request to get a participant session.
            name (str):
                Required. Resource name of the
                participant.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.types.ParticipantSession:
                [Developer Preview](\ https://developers.google.com/workspace/preview).
                   Refers to each unique join/leave session when a user
                   joins a conference from a device. Note that any time
                   a user joins the conference a new unique ID is
                   assigned. That means if a user joins a space multiple
                   times from the same device, they're assigned
                   different IDs, and are also be treated as different
                   participant sessions.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.GetParticipantSessionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetParticipantSessionRequest):
            request = service.GetParticipantSessionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_participant_session]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_participant_sessions(
        self,
        request: Optional[Union[service.ListParticipantSessionsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListParticipantSessionsPager:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the participant sessions of a participant in a conference
        record, by default ordered by join time and in descending order.
        This API supports ``fields`` as standard parameters like every
        other API. However, when the ``fields`` request parameter is
        omitted this API defaults to
        ``'participantsessions/*, next_page_token'``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_list_participant_sessions():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.ListParticipantSessionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_participant_sessions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.ListParticipantSessionsRequest, dict]):
                The request object. Request to fetch list of participant
                sessions per conference record per
                participant.
            parent (str):
                Required. Format:
                ``conferenceRecords/{conference_record}/participants/{participant}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.services.conference_records_service.pagers.ListParticipantSessionsPager:
                Response of ListParticipants method.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListParticipantSessionsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListParticipantSessionsRequest):
            request = service.ListParticipantSessionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_participant_sessions
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListParticipantSessionsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_recording(
        self,
        request: Optional[Union[service.GetRecordingRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resource.Recording:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a recording by recording ID.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_get_recording():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.GetRecordingRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_recording(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.GetRecordingRequest, dict]):
                The request object. Request message for GetRecording
                method.
            name (str):
                Required. Resource name of the
                recording.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.types.Recording:
                [Developer Preview](\ https://developers.google.com/workspace/preview).
                   Metadata about a recording created during a
                   conference.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.GetRecordingRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetRecordingRequest):
            request = service.GetRecordingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_recording]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_recordings(
        self,
        request: Optional[Union[service.ListRecordingsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRecordingsPager:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the recording resources from the conference record.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_list_recordings():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.ListRecordingsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_recordings(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.ListRecordingsRequest, dict]):
                The request object. Request for ListRecordings method.
            parent (str):
                Required. Format:
                ``conferenceRecords/{conference_record}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.services.conference_records_service.pagers.ListRecordingsPager:
                Response for ListRecordings method.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListRecordingsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListRecordingsRequest):
            request = service.ListRecordingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_recordings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListRecordingsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_transcript(
        self,
        request: Optional[Union[service.GetTranscriptRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resource.Transcript:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a transcript by transcript ID.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_get_transcript():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.GetTranscriptRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_transcript(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.GetTranscriptRequest, dict]):
                The request object. Request for GetTranscript method.
            name (str):
                Required. Resource name of the
                transcript.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.types.Transcript:
                [Developer Preview](\ https://developers.google.com/workspace/preview).
                   Metadata for a transcript generated from a
                   conference. It refers to the ASR (Automatic Speech
                   Recognition) result of user's speech during the
                   conference.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.GetTranscriptRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetTranscriptRequest):
            request = service.GetTranscriptRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_transcript]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_transcripts(
        self,
        request: Optional[Union[service.ListTranscriptsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTranscriptsPager:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the set of transcripts from the conference record.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_list_transcripts():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.ListTranscriptsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_transcripts(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.ListTranscriptsRequest, dict]):
                The request object. Request for ListTranscripts method.
            parent (str):
                Required. Format:
                ``conferenceRecords/{conference_record}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.services.conference_records_service.pagers.ListTranscriptsPager:
                Response for ListTranscripts method.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListTranscriptsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListTranscriptsRequest):
            request = service.ListTranscriptsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_transcripts]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTranscriptsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_transcript_entry(
        self,
        request: Optional[Union[service.GetTranscriptEntryRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resource.TranscriptEntry:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a ``TranscriptEntry`` resource by entry ID.

        Note: The transcript entries returned by the Google Meet API
        might not match the transcription found in the Google Docs
        transcript file. This can occur when the Google Docs transcript
        file is modified after generation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_get_transcript_entry():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.GetTranscriptEntryRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_transcript_entry(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.GetTranscriptEntryRequest, dict]):
                The request object. Request for GetTranscriptEntry
                method.
            name (str):
                Required. Resource name of the ``TranscriptEntry``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.types.TranscriptEntry:
                [Developer Preview](\ https://developers.google.com/workspace/preview).
                   Single entry for one user’s speech during a
                   transcript session.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.GetTranscriptEntryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetTranscriptEntryRequest):
            request = service.GetTranscriptEntryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_transcript_entry]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_transcript_entries(
        self,
        request: Optional[Union[service.ListTranscriptEntriesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTranscriptEntriesPager:
        r"""`Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the structured transcript entries per transcript. By
        default, ordered by start time and in ascending order.

        Note: The transcript entries returned by the Google Meet API
        might not match the transcription found in the Google Docs
        transcript file. This can occur when the Google Docs transcript
        file is modified after generation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import meet_v2beta

            def sample_list_transcript_entries():
                # Create a client
                client = meet_v2beta.ConferenceRecordsServiceClient()

                # Initialize request argument(s)
                request = meet_v2beta.ListTranscriptEntriesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_transcript_entries(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.meet_v2beta.types.ListTranscriptEntriesRequest, dict]):
                The request object. Request for ListTranscriptEntries
                method.
            parent (str):
                Required. Format:
                ``conferenceRecords/{conference_record}/transcripts/{transcript}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.meet_v2beta.services.conference_records_service.pagers.ListTranscriptEntriesPager:
                Response for ListTranscriptEntries
                method
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListTranscriptEntriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListTranscriptEntriesRequest):
            request = service.ListTranscriptEntriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_transcript_entries]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTranscriptEntriesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "ConferenceRecordsServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ConferenceRecordsServiceClient",)
