# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.shopping.merchant_conversions_v1beta.services.conversion_sources_service import (
    ConversionSourcesServiceAsyncClient,
    ConversionSourcesServiceClient,
    pagers,
    transports,
)
from google.shopping.merchant_conversions_v1beta.types import conversionsources


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert ConversionSourcesServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ConversionSourcesServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ConversionSourcesServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ConversionSourcesServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ConversionSourcesServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ConversionSourcesServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert ConversionSourcesServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert ConversionSourcesServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert ConversionSourcesServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            ConversionSourcesServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert ConversionSourcesServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert ConversionSourcesServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert ConversionSourcesServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            ConversionSourcesServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert ConversionSourcesServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert ConversionSourcesServiceClient._get_client_cert_source(None, False) is None
    assert (
        ConversionSourcesServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        ConversionSourcesServiceClient._get_client_cert_source(
            mock_provided_cert_source, True
        )
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                ConversionSourcesServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                ConversionSourcesServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    ConversionSourcesServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ConversionSourcesServiceClient),
)
@mock.patch.object(
    ConversionSourcesServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ConversionSourcesServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = ConversionSourcesServiceClient._DEFAULT_UNIVERSE
    default_endpoint = ConversionSourcesServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = ConversionSourcesServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        ConversionSourcesServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        ConversionSourcesServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == ConversionSourcesServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ConversionSourcesServiceClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        ConversionSourcesServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == ConversionSourcesServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ConversionSourcesServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == ConversionSourcesServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        ConversionSourcesServiceClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        ConversionSourcesServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        ConversionSourcesServiceClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        ConversionSourcesServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        ConversionSourcesServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        ConversionSourcesServiceClient._get_universe_domain(None, None)
        == ConversionSourcesServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        ConversionSourcesServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceGrpcTransport,
            "grpc",
        ),
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceRestTransport,
            "rest",
        ),
    ],
)
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(credentials=ga_credentials.AnonymousCredentials())
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        transport = transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # TODO: This is needed to cater for older versions of google-auth
    # Make this test unconditional once the minimum supported version of
    # google-auth becomes 2.23.0 or higher.
    google_auth_major, google_auth_minor = [
        int(part) for part in google.auth.__version__.split(".")[0:2]
    ]
    if google_auth_major > 2 or (google_auth_major == 2 and google_auth_minor >= 23):
        credentials = ga_credentials.AnonymousCredentials()
        credentials._universe_domain = "foo.com"
        # Test the case when there is a universe mismatch from the credentials.
        client = client_class(transport=transport_class(credentials=credentials))
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert (
            str(excinfo.value)
            == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
        )

        # Test the case when there is a universe mismatch from the client.
        #
        # TODO: Make this test unconditional once the minimum supported version of
        # google-api-core becomes 2.15.0 or higher.
        api_core_major, api_core_minor = [
            int(part) for part in api_core_version.__version__.split(".")[0:2]
        ]
        if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
            client = client_class(
                client_options={"universe_domain": "bar.com"},
                transport=transport_class(
                    credentials=ga_credentials.AnonymousCredentials(),
                ),
            )
            with pytest.raises(ValueError) as excinfo:
                client._validate_universe_domain()
            assert (
                str(excinfo.value)
                == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
            )

    # Test that ValueError is raised if universe_domain is provided via client options and credentials is None
    with pytest.raises(ValueError):
        client._compare_universes("foo.bar", None)


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ConversionSourcesServiceClient, "grpc"),
        (ConversionSourcesServiceAsyncClient, "grpc_asyncio"),
        (ConversionSourcesServiceClient, "rest"),
    ],
)
def test_conversion_sources_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "merchantapi.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://merchantapi.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ConversionSourcesServiceGrpcTransport, "grpc"),
        (transports.ConversionSourcesServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.ConversionSourcesServiceRestTransport, "rest"),
    ],
)
def test_conversion_sources_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ConversionSourcesServiceClient, "grpc"),
        (ConversionSourcesServiceAsyncClient, "grpc_asyncio"),
        (ConversionSourcesServiceClient, "rest"),
    ],
)
def test_conversion_sources_service_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "merchantapi.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://merchantapi.googleapis.com"
        )


def test_conversion_sources_service_client_get_transport_class():
    transport = ConversionSourcesServiceClient.get_transport_class()
    available_transports = [
        transports.ConversionSourcesServiceGrpcTransport,
        transports.ConversionSourcesServiceRestTransport,
    ]
    assert transport in available_transports

    transport = ConversionSourcesServiceClient.get_transport_class("grpc")
    assert transport == transports.ConversionSourcesServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceGrpcTransport,
            "grpc",
        ),
        (
            ConversionSourcesServiceAsyncClient,
            transports.ConversionSourcesServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    ConversionSourcesServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ConversionSourcesServiceClient),
)
@mock.patch.object(
    ConversionSourcesServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ConversionSourcesServiceAsyncClient),
)
def test_conversion_sources_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        ConversionSourcesServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        ConversionSourcesServiceClient, "get_transport_class"
    ) as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            ConversionSourcesServiceAsyncClient,
            transports.ConversionSourcesServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            ConversionSourcesServiceAsyncClient,
            transports.ConversionSourcesServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceRestTransport,
            "rest",
            "true",
        ),
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    ConversionSourcesServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ConversionSourcesServiceClient),
)
@mock.patch.object(
    ConversionSourcesServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ConversionSourcesServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_conversion_sources_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class",
    [ConversionSourcesServiceClient, ConversionSourcesServiceAsyncClient],
)
@mock.patch.object(
    ConversionSourcesServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ConversionSourcesServiceClient),
)
@mock.patch.object(
    ConversionSourcesServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ConversionSourcesServiceAsyncClient),
)
def test_conversion_sources_service_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize(
    "client_class",
    [ConversionSourcesServiceClient, ConversionSourcesServiceAsyncClient],
)
@mock.patch.object(
    ConversionSourcesServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ConversionSourcesServiceClient),
)
@mock.patch.object(
    ConversionSourcesServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(ConversionSourcesServiceAsyncClient),
)
def test_conversion_sources_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = ConversionSourcesServiceClient._DEFAULT_UNIVERSE
    default_endpoint = ConversionSourcesServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = ConversionSourcesServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceGrpcTransport,
            "grpc",
        ),
        (
            ConversionSourcesServiceAsyncClient,
            transports.ConversionSourcesServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceRestTransport,
            "rest",
        ),
    ],
)
def test_conversion_sources_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ConversionSourcesServiceAsyncClient,
            transports.ConversionSourcesServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_conversion_sources_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_conversion_sources_service_client_client_options_from_dict():
    with mock.patch(
        "google.shopping.merchant_conversions_v1beta.services.conversion_sources_service.transports.ConversionSourcesServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ConversionSourcesServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ConversionSourcesServiceAsyncClient,
            transports.ConversionSourcesServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_conversion_sources_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "merchantapi.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/content",),
            scopes=None,
            default_host="merchantapi.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.CreateConversionSourceRequest,
        dict,
    ],
)
def test_create_conversion_source(request_type, transport: str = "grpc"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource(
            name="name_value",
            state=conversionsources.ConversionSource.State.ACTIVE,
            controller=conversionsources.ConversionSource.Controller.MERCHANT,
        )
        response = client.create_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = conversionsources.CreateConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


def test_create_conversion_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.CreateConversionSourceRequest()


def test_create_conversion_source_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = conversionsources.CreateConversionSourceRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_conversion_source(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.CreateConversionSourceRequest(
            parent="parent_value",
        )


def test_create_conversion_source_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_conversion_source
        ] = mock_rpc
        request = {}
        client.create_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_conversion_source_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource(
                name="name_value",
                state=conversionsources.ConversionSource.State.ACTIVE,
                controller=conversionsources.ConversionSource.Controller.MERCHANT,
            )
        )
        response = await client.create_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.CreateConversionSourceRequest()


@pytest.mark.asyncio
async def test_create_conversion_source_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_conversion_source
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_conversion_source
        ] = mock_object

        request = {}
        await client.create_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.create_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_conversion_source_async(
    transport: str = "grpc_asyncio",
    request_type=conversionsources.CreateConversionSourceRequest,
):
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource(
                name="name_value",
                state=conversionsources.ConversionSource.State.ACTIVE,
                controller=conversionsources.ConversionSource.Controller.MERCHANT,
            )
        )
        response = await client.create_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = conversionsources.CreateConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


@pytest.mark.asyncio
async def test_create_conversion_source_async_from_dict():
    await test_create_conversion_source_async(request_type=dict)


def test_create_conversion_source_field_headers():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.CreateConversionSourceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        call.return_value = conversionsources.ConversionSource()
        client.create_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_conversion_source_field_headers_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.CreateConversionSourceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource()
        )
        await client.create_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_conversion_source_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_conversion_source(
            parent="parent_value",
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].conversion_source
        mock_val = conversionsources.ConversionSource(
            google_analytics_link=conversionsources.GoogleAnalyticsLink(
                property_id=1201
            )
        )
        assert arg == mock_val


def test_create_conversion_source_flattened_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_conversion_source(
            conversionsources.CreateConversionSourceRequest(),
            parent="parent_value",
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
        )


@pytest.mark.asyncio
async def test_create_conversion_source_flattened_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_conversion_source(
            parent="parent_value",
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].conversion_source
        mock_val = conversionsources.ConversionSource(
            google_analytics_link=conversionsources.GoogleAnalyticsLink(
                property_id=1201
            )
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_conversion_source_flattened_error_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_conversion_source(
            conversionsources.CreateConversionSourceRequest(),
            parent="parent_value",
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.UpdateConversionSourceRequest,
        dict,
    ],
)
def test_update_conversion_source(request_type, transport: str = "grpc"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource(
            name="name_value",
            state=conversionsources.ConversionSource.State.ACTIVE,
            controller=conversionsources.ConversionSource.Controller.MERCHANT,
        )
        response = client.update_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = conversionsources.UpdateConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


def test_update_conversion_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.UpdateConversionSourceRequest()


def test_update_conversion_source_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = conversionsources.UpdateConversionSourceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_conversion_source(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.UpdateConversionSourceRequest()


def test_update_conversion_source_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_conversion_source
        ] = mock_rpc
        request = {}
        client.update_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_conversion_source_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource(
                name="name_value",
                state=conversionsources.ConversionSource.State.ACTIVE,
                controller=conversionsources.ConversionSource.Controller.MERCHANT,
            )
        )
        response = await client.update_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.UpdateConversionSourceRequest()


@pytest.mark.asyncio
async def test_update_conversion_source_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_conversion_source
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_conversion_source
        ] = mock_object

        request = {}
        await client.update_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.update_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_conversion_source_async(
    transport: str = "grpc_asyncio",
    request_type=conversionsources.UpdateConversionSourceRequest,
):
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource(
                name="name_value",
                state=conversionsources.ConversionSource.State.ACTIVE,
                controller=conversionsources.ConversionSource.Controller.MERCHANT,
            )
        )
        response = await client.update_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = conversionsources.UpdateConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


@pytest.mark.asyncio
async def test_update_conversion_source_async_from_dict():
    await test_update_conversion_source_async(request_type=dict)


def test_update_conversion_source_field_headers():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.UpdateConversionSourceRequest()

    request.conversion_source.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        call.return_value = conversionsources.ConversionSource()
        client.update_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_source.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_conversion_source_field_headers_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.UpdateConversionSourceRequest()

    request.conversion_source.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource()
        )
        await client.update_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_source.name=name_value",
    ) in kw["metadata"]


def test_update_conversion_source_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_conversion_source(
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].conversion_source
        mock_val = conversionsources.ConversionSource(
            google_analytics_link=conversionsources.GoogleAnalyticsLink(
                property_id=1201
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_conversion_source_flattened_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_conversion_source(
            conversionsources.UpdateConversionSourceRequest(),
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_conversion_source_flattened_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_conversion_source(
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].conversion_source
        mock_val = conversionsources.ConversionSource(
            google_analytics_link=conversionsources.GoogleAnalyticsLink(
                property_id=1201
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_conversion_source_flattened_error_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_conversion_source(
            conversionsources.UpdateConversionSourceRequest(),
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.DeleteConversionSourceRequest,
        dict,
    ],
)
def test_delete_conversion_source(request_type, transport: str = "grpc"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = conversionsources.DeleteConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_conversion_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.DeleteConversionSourceRequest()


def test_delete_conversion_source_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = conversionsources.DeleteConversionSourceRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_conversion_source(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.DeleteConversionSourceRequest(
            name="name_value",
        )


def test_delete_conversion_source_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_conversion_source
        ] = mock_rpc
        request = {}
        client.delete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_conversion_source_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.DeleteConversionSourceRequest()


@pytest.mark.asyncio
async def test_delete_conversion_source_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_conversion_source
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_conversion_source
        ] = mock_object

        request = {}
        await client.delete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.delete_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_conversion_source_async(
    transport: str = "grpc_asyncio",
    request_type=conversionsources.DeleteConversionSourceRequest,
):
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = conversionsources.DeleteConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_conversion_source_async_from_dict():
    await test_delete_conversion_source_async(request_type=dict)


def test_delete_conversion_source_field_headers():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.DeleteConversionSourceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        call.return_value = None
        client.delete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_conversion_source_field_headers_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.DeleteConversionSourceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_conversion_source_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_conversion_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_conversion_source_flattened_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_conversion_source(
            conversionsources.DeleteConversionSourceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_conversion_source_flattened_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_conversion_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_conversion_source_flattened_error_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_conversion_source(
            conversionsources.DeleteConversionSourceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.UndeleteConversionSourceRequest,
        dict,
    ],
)
def test_undelete_conversion_source(request_type, transport: str = "grpc"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource(
            name="name_value",
            state=conversionsources.ConversionSource.State.ACTIVE,
            controller=conversionsources.ConversionSource.Controller.MERCHANT,
        )
        response = client.undelete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = conversionsources.UndeleteConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


def test_undelete_conversion_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.undelete_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.UndeleteConversionSourceRequest()


def test_undelete_conversion_source_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = conversionsources.UndeleteConversionSourceRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.undelete_conversion_source(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.UndeleteConversionSourceRequest(
            name="name_value",
        )


def test_undelete_conversion_source_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.undelete_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.undelete_conversion_source
        ] = mock_rpc
        request = {}
        client.undelete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.undelete_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_undelete_conversion_source_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource(
                name="name_value",
                state=conversionsources.ConversionSource.State.ACTIVE,
                controller=conversionsources.ConversionSource.Controller.MERCHANT,
            )
        )
        response = await client.undelete_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.UndeleteConversionSourceRequest()


@pytest.mark.asyncio
async def test_undelete_conversion_source_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.undelete_conversion_source
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.undelete_conversion_source
        ] = mock_object

        request = {}
        await client.undelete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.undelete_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_undelete_conversion_source_async(
    transport: str = "grpc_asyncio",
    request_type=conversionsources.UndeleteConversionSourceRequest,
):
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource(
                name="name_value",
                state=conversionsources.ConversionSource.State.ACTIVE,
                controller=conversionsources.ConversionSource.Controller.MERCHANT,
            )
        )
        response = await client.undelete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = conversionsources.UndeleteConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


@pytest.mark.asyncio
async def test_undelete_conversion_source_async_from_dict():
    await test_undelete_conversion_source_async(request_type=dict)


def test_undelete_conversion_source_field_headers():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.UndeleteConversionSourceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_conversion_source), "__call__"
    ) as call:
        call.return_value = conversionsources.ConversionSource()
        client.undelete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_undelete_conversion_source_field_headers_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.UndeleteConversionSourceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_conversion_source), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource()
        )
        await client.undelete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.GetConversionSourceRequest,
        dict,
    ],
)
def test_get_conversion_source(request_type, transport: str = "grpc"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource(
            name="name_value",
            state=conversionsources.ConversionSource.State.ACTIVE,
            controller=conversionsources.ConversionSource.Controller.MERCHANT,
        )
        response = client.get_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = conversionsources.GetConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


def test_get_conversion_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.GetConversionSourceRequest()


def test_get_conversion_source_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = conversionsources.GetConversionSourceRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_conversion_source(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.GetConversionSourceRequest(
            name="name_value",
        )


def test_get_conversion_source_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_conversion_source
        ] = mock_rpc
        request = {}
        client.get_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_conversion_source_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource(
                name="name_value",
                state=conversionsources.ConversionSource.State.ACTIVE,
                controller=conversionsources.ConversionSource.Controller.MERCHANT,
            )
        )
        response = await client.get_conversion_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.GetConversionSourceRequest()


@pytest.mark.asyncio
async def test_get_conversion_source_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_conversion_source
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_conversion_source
        ] = mock_object

        request = {}
        await client.get_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_conversion_source_async(
    transport: str = "grpc_asyncio",
    request_type=conversionsources.GetConversionSourceRequest,
):
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource(
                name="name_value",
                state=conversionsources.ConversionSource.State.ACTIVE,
                controller=conversionsources.ConversionSource.Controller.MERCHANT,
            )
        )
        response = await client.get_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = conversionsources.GetConversionSourceRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


@pytest.mark.asyncio
async def test_get_conversion_source_async_from_dict():
    await test_get_conversion_source_async(request_type=dict)


def test_get_conversion_source_field_headers():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.GetConversionSourceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        call.return_value = conversionsources.ConversionSource()
        client.get_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_conversion_source_field_headers_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.GetConversionSourceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource()
        )
        await client.get_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_conversion_source_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_conversion_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_conversion_source_flattened_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_conversion_source(
            conversionsources.GetConversionSourceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_conversion_source_flattened_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_source), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ConversionSource()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ConversionSource()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_conversion_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_conversion_source_flattened_error_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_conversion_source(
            conversionsources.GetConversionSourceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.ListConversionSourcesRequest,
        dict,
    ],
)
def test_list_conversion_sources(request_type, transport: str = "grpc"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ListConversionSourcesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_conversion_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = conversionsources.ListConversionSourcesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionSourcesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_conversion_sources_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_conversion_sources()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.ListConversionSourcesRequest()


def test_list_conversion_sources_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = conversionsources.ListConversionSourcesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_conversion_sources(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.ListConversionSourcesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_conversion_sources_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_conversion_sources
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_conversion_sources
        ] = mock_rpc
        request = {}
        client.list_conversion_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_conversion_sources(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_conversion_sources_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ListConversionSourcesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_conversion_sources()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == conversionsources.ListConversionSourcesRequest()


@pytest.mark.asyncio
async def test_list_conversion_sources_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_conversion_sources
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_conversion_sources
        ] = mock_object

        request = {}
        await client.list_conversion_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_conversion_sources(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_conversion_sources_async(
    transport: str = "grpc_asyncio",
    request_type=conversionsources.ListConversionSourcesRequest,
):
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ListConversionSourcesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_conversion_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = conversionsources.ListConversionSourcesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionSourcesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_conversion_sources_async_from_dict():
    await test_list_conversion_sources_async(request_type=dict)


def test_list_conversion_sources_field_headers():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.ListConversionSourcesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        call.return_value = conversionsources.ListConversionSourcesResponse()
        client.list_conversion_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_conversion_sources_field_headers_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = conversionsources.ListConversionSourcesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ListConversionSourcesResponse()
        )
        await client.list_conversion_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_conversion_sources_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ListConversionSourcesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_conversion_sources(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_conversion_sources_flattened_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_conversion_sources(
            conversionsources.ListConversionSourcesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_conversion_sources_flattened_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionsources.ListConversionSourcesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionsources.ListConversionSourcesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_conversion_sources(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_conversion_sources_flattened_error_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_conversion_sources(
            conversionsources.ListConversionSourcesRequest(),
            parent="parent_value",
        )


def test_list_conversion_sources_pager(transport_name: str = "grpc"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
                next_page_token="abc",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[],
                next_page_token="def",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                ],
                next_page_token="ghi",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_conversion_sources(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, conversionsources.ConversionSource) for i in results)


def test_list_conversion_sources_pages(transport_name: str = "grpc"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
                next_page_token="abc",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[],
                next_page_token="def",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                ],
                next_page_token="ghi",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_conversion_sources(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_conversion_sources_async_pager():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
                next_page_token="abc",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[],
                next_page_token="def",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                ],
                next_page_token="ghi",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_conversion_sources(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, conversionsources.ConversionSource) for i in responses)


@pytest.mark.asyncio
async def test_list_conversion_sources_async_pages():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_sources),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
                next_page_token="abc",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[],
                next_page_token="def",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                ],
                next_page_token="ghi",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_conversion_sources(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.CreateConversionSourceRequest,
        dict,
    ],
)
def test_create_conversion_source_rest(request_type):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "accounts/sample1"}
    request_init["conversion_source"] = {
        "google_analytics_link": {
            "property_id": 1201,
            "attribution_settings": {
                "attribution_lookback_window_days": 3425,
                "attribution_model": 1,
                "conversion_type": [{"name": "name_value", "report": True}],
            },
            "property": "property_value",
        },
        "merchant_center_destination": {
            "destination": "destination_value",
            "attribution_settings": {},
            "display_name": "display_name_value",
            "currency_code": "currency_code_value",
        },
        "name": "name_value",
        "state": 1,
        "expire_time": {"seconds": 751, "nanos": 543},
        "controller": 1,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = conversionsources.CreateConversionSourceRequest.meta.fields[
        "conversion_source"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["conversion_source"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["conversion_source"][field])):
                    del request_init["conversion_source"][field][i][subfield]
            else:
                del request_init["conversion_source"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ConversionSource(
            name="name_value",
            state=conversionsources.ConversionSource.State.ACTIVE,
            controller=conversionsources.ConversionSource.Controller.MERCHANT,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ConversionSource.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_conversion_source(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


def test_create_conversion_source_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_conversion_source
        ] = mock_rpc

        request = {}
        client.create_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_conversion_source_rest_required_fields(
    request_type=conversionsources.CreateConversionSourceRequest,
):
    transport_class = transports.ConversionSourcesServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = conversionsources.ConversionSource()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = conversionsources.ConversionSource.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_conversion_source(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_conversion_source_rest_unset_required_fields():
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_conversion_source._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "conversionSource",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_conversion_source_rest_interceptors(null_interceptor):
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ConversionSourcesServiceRestInterceptor(),
    )
    client = ConversionSourcesServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "post_create_conversion_source",
    ) as post, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "pre_create_conversion_source",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = conversionsources.CreateConversionSourceRequest.pb(
            conversionsources.CreateConversionSourceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = conversionsources.ConversionSource.to_json(
            conversionsources.ConversionSource()
        )

        request = conversionsources.CreateConversionSourceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = conversionsources.ConversionSource()

        client.create_conversion_source(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_conversion_source_rest_bad_request(
    transport: str = "rest",
    request_type=conversionsources.CreateConversionSourceRequest,
):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "accounts/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_conversion_source(request)


def test_create_conversion_source_rest_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ConversionSource()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "accounts/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ConversionSource.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_conversion_source(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/conversions/v1beta/{parent=accounts/*}/conversionSources"
            % client.transport._host,
            args[1],
        )


def test_create_conversion_source_rest_flattened_error(transport: str = "rest"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_conversion_source(
            conversionsources.CreateConversionSourceRequest(),
            parent="parent_value",
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
        )


def test_create_conversion_source_rest_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.UpdateConversionSourceRequest,
        dict,
    ],
)
def test_update_conversion_source_rest(request_type):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "conversion_source": {"name": "accounts/sample1/conversionSources/sample2"}
    }
    request_init["conversion_source"] = {
        "google_analytics_link": {
            "property_id": 1201,
            "attribution_settings": {
                "attribution_lookback_window_days": 3425,
                "attribution_model": 1,
                "conversion_type": [{"name": "name_value", "report": True}],
            },
            "property": "property_value",
        },
        "merchant_center_destination": {
            "destination": "destination_value",
            "attribution_settings": {},
            "display_name": "display_name_value",
            "currency_code": "currency_code_value",
        },
        "name": "accounts/sample1/conversionSources/sample2",
        "state": 1,
        "expire_time": {"seconds": 751, "nanos": 543},
        "controller": 1,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = conversionsources.UpdateConversionSourceRequest.meta.fields[
        "conversion_source"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["conversion_source"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["conversion_source"][field])):
                    del request_init["conversion_source"][field][i][subfield]
            else:
                del request_init["conversion_source"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ConversionSource(
            name="name_value",
            state=conversionsources.ConversionSource.State.ACTIVE,
            controller=conversionsources.ConversionSource.Controller.MERCHANT,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ConversionSource.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_conversion_source(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


def test_update_conversion_source_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_conversion_source
        ] = mock_rpc

        request = {}
        client.update_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_conversion_source_rest_required_fields(
    request_type=conversionsources.UpdateConversionSourceRequest,
):
    transport_class = transports.ConversionSourcesServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_conversion_source._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = conversionsources.ConversionSource()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = conversionsources.ConversionSource.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_conversion_source(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_conversion_source_rest_unset_required_fields():
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_conversion_source._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "conversionSource",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_conversion_source_rest_interceptors(null_interceptor):
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ConversionSourcesServiceRestInterceptor(),
    )
    client = ConversionSourcesServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "post_update_conversion_source",
    ) as post, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "pre_update_conversion_source",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = conversionsources.UpdateConversionSourceRequest.pb(
            conversionsources.UpdateConversionSourceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = conversionsources.ConversionSource.to_json(
            conversionsources.ConversionSource()
        )

        request = conversionsources.UpdateConversionSourceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = conversionsources.ConversionSource()

        client.update_conversion_source(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_conversion_source_rest_bad_request(
    transport: str = "rest",
    request_type=conversionsources.UpdateConversionSourceRequest,
):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "conversion_source": {"name": "accounts/sample1/conversionSources/sample2"}
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_conversion_source(request)


def test_update_conversion_source_rest_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ConversionSource()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "conversion_source": {"name": "accounts/sample1/conversionSources/sample2"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ConversionSource.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_conversion_source(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/conversions/v1beta/{conversion_source.name=accounts/*/conversionSources/*}"
            % client.transport._host,
            args[1],
        )


def test_update_conversion_source_rest_flattened_error(transport: str = "rest"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_conversion_source(
            conversionsources.UpdateConversionSourceRequest(),
            conversion_source=conversionsources.ConversionSource(
                google_analytics_link=conversionsources.GoogleAnalyticsLink(
                    property_id=1201
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_conversion_source_rest_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.DeleteConversionSourceRequest,
        dict,
    ],
)
def test_delete_conversion_source_rest(request_type):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/conversionSources/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_conversion_source(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_conversion_source_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_conversion_source
        ] = mock_rpc

        request = {}
        client.delete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_conversion_source_rest_required_fields(
    request_type=conversionsources.DeleteConversionSourceRequest,
):
    transport_class = transports.ConversionSourcesServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_conversion_source(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_conversion_source_rest_unset_required_fields():
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_conversion_source._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_conversion_source_rest_interceptors(null_interceptor):
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ConversionSourcesServiceRestInterceptor(),
    )
    client = ConversionSourcesServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "pre_delete_conversion_source",
    ) as pre:
        pre.assert_not_called()
        pb_message = conversionsources.DeleteConversionSourceRequest.pb(
            conversionsources.DeleteConversionSourceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = conversionsources.DeleteConversionSourceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_conversion_source(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_conversion_source_rest_bad_request(
    transport: str = "rest",
    request_type=conversionsources.DeleteConversionSourceRequest,
):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/conversionSources/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_conversion_source(request)


def test_delete_conversion_source_rest_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "accounts/sample1/conversionSources/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_conversion_source(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/conversions/v1beta/{name=accounts/*/conversionSources/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_conversion_source_rest_flattened_error(transport: str = "rest"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_conversion_source(
            conversionsources.DeleteConversionSourceRequest(),
            name="name_value",
        )


def test_delete_conversion_source_rest_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.UndeleteConversionSourceRequest,
        dict,
    ],
)
def test_undelete_conversion_source_rest(request_type):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/conversionSources/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ConversionSource(
            name="name_value",
            state=conversionsources.ConversionSource.State.ACTIVE,
            controller=conversionsources.ConversionSource.Controller.MERCHANT,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ConversionSource.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.undelete_conversion_source(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


def test_undelete_conversion_source_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.undelete_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.undelete_conversion_source
        ] = mock_rpc

        request = {}
        client.undelete_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.undelete_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_undelete_conversion_source_rest_required_fields(
    request_type=conversionsources.UndeleteConversionSourceRequest,
):
    transport_class = transports.ConversionSourcesServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).undelete_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).undelete_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = conversionsources.ConversionSource()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = conversionsources.ConversionSource.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.undelete_conversion_source(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_undelete_conversion_source_rest_unset_required_fields():
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.undelete_conversion_source._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_undelete_conversion_source_rest_interceptors(null_interceptor):
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ConversionSourcesServiceRestInterceptor(),
    )
    client = ConversionSourcesServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "post_undelete_conversion_source",
    ) as post, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "pre_undelete_conversion_source",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = conversionsources.UndeleteConversionSourceRequest.pb(
            conversionsources.UndeleteConversionSourceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = conversionsources.ConversionSource.to_json(
            conversionsources.ConversionSource()
        )

        request = conversionsources.UndeleteConversionSourceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = conversionsources.ConversionSource()

        client.undelete_conversion_source(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_undelete_conversion_source_rest_bad_request(
    transport: str = "rest",
    request_type=conversionsources.UndeleteConversionSourceRequest,
):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/conversionSources/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.undelete_conversion_source(request)


def test_undelete_conversion_source_rest_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.GetConversionSourceRequest,
        dict,
    ],
)
def test_get_conversion_source_rest(request_type):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/conversionSources/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ConversionSource(
            name="name_value",
            state=conversionsources.ConversionSource.State.ACTIVE,
            controller=conversionsources.ConversionSource.Controller.MERCHANT,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ConversionSource.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_conversion_source(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionsources.ConversionSource)
    assert response.name == "name_value"
    assert response.state == conversionsources.ConversionSource.State.ACTIVE
    assert response.controller == conversionsources.ConversionSource.Controller.MERCHANT


def test_get_conversion_source_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_conversion_source
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_conversion_source
        ] = mock_rpc

        request = {}
        client.get_conversion_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_conversion_source(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_conversion_source_rest_required_fields(
    request_type=conversionsources.GetConversionSourceRequest,
):
    transport_class = transports.ConversionSourcesServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_conversion_source._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = conversionsources.ConversionSource()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = conversionsources.ConversionSource.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_conversion_source(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_conversion_source_rest_unset_required_fields():
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_conversion_source._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_conversion_source_rest_interceptors(null_interceptor):
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ConversionSourcesServiceRestInterceptor(),
    )
    client = ConversionSourcesServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor, "post_get_conversion_source"
    ) as post, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor, "pre_get_conversion_source"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = conversionsources.GetConversionSourceRequest.pb(
            conversionsources.GetConversionSourceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = conversionsources.ConversionSource.to_json(
            conversionsources.ConversionSource()
        )

        request = conversionsources.GetConversionSourceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = conversionsources.ConversionSource()

        client.get_conversion_source(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_conversion_source_rest_bad_request(
    transport: str = "rest", request_type=conversionsources.GetConversionSourceRequest
):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/conversionSources/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_conversion_source(request)


def test_get_conversion_source_rest_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ConversionSource()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "accounts/sample1/conversionSources/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ConversionSource.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_conversion_source(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/conversions/v1beta/{name=accounts/*/conversionSources/*}"
            % client.transport._host,
            args[1],
        )


def test_get_conversion_source_rest_flattened_error(transport: str = "rest"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_conversion_source(
            conversionsources.GetConversionSourceRequest(),
            name="name_value",
        )


def test_get_conversion_source_rest_error():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        conversionsources.ListConversionSourcesRequest,
        dict,
    ],
)
def test_list_conversion_sources_rest(request_type):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "accounts/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ListConversionSourcesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ListConversionSourcesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_conversion_sources(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionSourcesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_conversion_sources_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_conversion_sources
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_conversion_sources
        ] = mock_rpc

        request = {}
        client.list_conversion_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_conversion_sources(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_conversion_sources_rest_required_fields(
    request_type=conversionsources.ListConversionSourcesRequest,
):
    transport_class = transports.ConversionSourcesServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_conversion_sources._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_conversion_sources._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "show_deleted",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = conversionsources.ListConversionSourcesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = conversionsources.ListConversionSourcesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_conversion_sources(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_conversion_sources_rest_unset_required_fields():
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_conversion_sources._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "showDeleted",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_conversion_sources_rest_interceptors(null_interceptor):
    transport = transports.ConversionSourcesServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ConversionSourcesServiceRestInterceptor(),
    )
    client = ConversionSourcesServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "post_list_conversion_sources",
    ) as post, mock.patch.object(
        transports.ConversionSourcesServiceRestInterceptor,
        "pre_list_conversion_sources",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = conversionsources.ListConversionSourcesRequest.pb(
            conversionsources.ListConversionSourcesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            conversionsources.ListConversionSourcesResponse.to_json(
                conversionsources.ListConversionSourcesResponse()
            )
        )

        request = conversionsources.ListConversionSourcesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = conversionsources.ListConversionSourcesResponse()

        client.list_conversion_sources(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_conversion_sources_rest_bad_request(
    transport: str = "rest", request_type=conversionsources.ListConversionSourcesRequest
):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "accounts/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_conversion_sources(request)


def test_list_conversion_sources_rest_flattened():
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = conversionsources.ListConversionSourcesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "accounts/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = conversionsources.ListConversionSourcesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_conversion_sources(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/conversions/v1beta/{parent=accounts/*}/conversionSources"
            % client.transport._host,
            args[1],
        )


def test_list_conversion_sources_rest_flattened_error(transport: str = "rest"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_conversion_sources(
            conversionsources.ListConversionSourcesRequest(),
            parent="parent_value",
        )


def test_list_conversion_sources_rest_pager(transport: str = "rest"):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
                next_page_token="abc",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[],
                next_page_token="def",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                ],
                next_page_token="ghi",
            ),
            conversionsources.ListConversionSourcesResponse(
                conversion_sources=[
                    conversionsources.ConversionSource(),
                    conversionsources.ConversionSource(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            conversionsources.ListConversionSourcesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "accounts/sample1"}

        pager = client.list_conversion_sources(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, conversionsources.ConversionSource) for i in results)

        pages = list(client.list_conversion_sources(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ConversionSourcesServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ConversionSourcesServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConversionSourcesServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ConversionSourcesServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ConversionSourcesServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ConversionSourcesServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ConversionSourcesServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ConversionSourcesServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ConversionSourcesServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ConversionSourcesServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ConversionSourcesServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ConversionSourcesServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversionSourcesServiceGrpcTransport,
        transports.ConversionSourcesServiceGrpcAsyncIOTransport,
        transports.ConversionSourcesServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = ConversionSourcesServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ConversionSourcesServiceGrpcTransport,
    )


def test_conversion_sources_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ConversionSourcesServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_conversion_sources_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.shopping.merchant_conversions_v1beta.services.conversion_sources_service.transports.ConversionSourcesServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ConversionSourcesServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_conversion_source",
        "update_conversion_source",
        "delete_conversion_source",
        "undelete_conversion_source",
        "get_conversion_source",
        "list_conversion_sources",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_conversion_sources_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.shopping.merchant_conversions_v1beta.services.conversion_sources_service.transports.ConversionSourcesServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ConversionSourcesServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/content",),
            quota_project_id="octopus",
        )


def test_conversion_sources_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.shopping.merchant_conversions_v1beta.services.conversion_sources_service.transports.ConversionSourcesServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ConversionSourcesServiceTransport()
        adc.assert_called_once()


def test_conversion_sources_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ConversionSourcesServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/content",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversionSourcesServiceGrpcTransport,
        transports.ConversionSourcesServiceGrpcAsyncIOTransport,
    ],
)
def test_conversion_sources_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/content",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversionSourcesServiceGrpcTransport,
        transports.ConversionSourcesServiceGrpcAsyncIOTransport,
        transports.ConversionSourcesServiceRestTransport,
    ],
)
def test_conversion_sources_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.ConversionSourcesServiceGrpcTransport, grpc_helpers),
        (transports.ConversionSourcesServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_conversion_sources_service_transport_create_channel(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "merchantapi.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/content",),
            scopes=["1", "2"],
            default_host="merchantapi.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversionSourcesServiceGrpcTransport,
        transports.ConversionSourcesServiceGrpcAsyncIOTransport,
    ],
)
def test_conversion_sources_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_conversion_sources_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.ConversionSourcesServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_conversion_sources_service_host_no_port(transport_name):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="merchantapi.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "merchantapi.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://merchantapi.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_conversion_sources_service_host_with_port(transport_name):
    client = ConversionSourcesServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="merchantapi.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "merchantapi.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://merchantapi.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_conversion_sources_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = ConversionSourcesServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = ConversionSourcesServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_conversion_source._session
    session2 = client2.transport.create_conversion_source._session
    assert session1 != session2
    session1 = client1.transport.update_conversion_source._session
    session2 = client2.transport.update_conversion_source._session
    assert session1 != session2
    session1 = client1.transport.delete_conversion_source._session
    session2 = client2.transport.delete_conversion_source._session
    assert session1 != session2
    session1 = client1.transport.undelete_conversion_source._session
    session2 = client2.transport.undelete_conversion_source._session
    assert session1 != session2
    session1 = client1.transport.get_conversion_source._session
    session2 = client2.transport.get_conversion_source._session
    assert session1 != session2
    session1 = client1.transport.list_conversion_sources._session
    session2 = client2.transport.list_conversion_sources._session
    assert session1 != session2


def test_conversion_sources_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ConversionSourcesServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_conversion_sources_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ConversionSourcesServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversionSourcesServiceGrpcTransport,
        transports.ConversionSourcesServiceGrpcAsyncIOTransport,
    ],
)
def test_conversion_sources_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ConversionSourcesServiceGrpcTransport,
        transports.ConversionSourcesServiceGrpcAsyncIOTransport,
    ],
)
def test_conversion_sources_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_conversion_source_path():
    account = "squid"
    conversion_source = "clam"
    expected = "accounts/{account}/conversionSources/{conversion_source}".format(
        account=account,
        conversion_source=conversion_source,
    )
    actual = ConversionSourcesServiceClient.conversion_source_path(
        account, conversion_source
    )
    assert expected == actual


def test_parse_conversion_source_path():
    expected = {
        "account": "whelk",
        "conversion_source": "octopus",
    }
    path = ConversionSourcesServiceClient.conversion_source_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversionSourcesServiceClient.parse_conversion_source_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ConversionSourcesServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = ConversionSourcesServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversionSourcesServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ConversionSourcesServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = ConversionSourcesServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversionSourcesServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ConversionSourcesServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = ConversionSourcesServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversionSourcesServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ConversionSourcesServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = ConversionSourcesServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversionSourcesServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ConversionSourcesServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = ConversionSourcesServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ConversionSourcesServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ConversionSourcesServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ConversionSourcesServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ConversionSourcesServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = ConversionSourcesServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = ConversionSourcesServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (
            ConversionSourcesServiceClient,
            transports.ConversionSourcesServiceGrpcTransport,
        ),
        (
            ConversionSourcesServiceAsyncClient,
            transports.ConversionSourcesServiceGrpcAsyncIOTransport,
        ),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
