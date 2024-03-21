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
from google.cloud.storage_client import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.storage_client_v2.services.storage.async_client import (
    StorageAsyncClient,
)
from google.cloud.storage_client_v2.services.storage.client import StorageClient
from google.cloud.storage_client_v2.types.storage import (
    BidiWriteObjectRequest,
    BidiWriteObjectResponse,
    Bucket,
    BucketAccessControl,
    CancelResumableWriteRequest,
    CancelResumableWriteResponse,
    ChecksummedData,
    CommonObjectRequestParams,
    ComposeObjectRequest,
    ContentRange,
    CreateBucketRequest,
    CreateHmacKeyRequest,
    CreateHmacKeyResponse,
    CreateNotificationConfigRequest,
    CustomerEncryption,
    DeleteBucketRequest,
    DeleteHmacKeyRequest,
    DeleteNotificationConfigRequest,
    DeleteObjectRequest,
    GetBucketRequest,
    GetHmacKeyRequest,
    GetNotificationConfigRequest,
    GetObjectRequest,
    GetServiceAccountRequest,
    HmacKeyMetadata,
    ListBucketsRequest,
    ListBucketsResponse,
    ListHmacKeysRequest,
    ListHmacKeysResponse,
    ListNotificationConfigsRequest,
    ListNotificationConfigsResponse,
    ListObjectsRequest,
    ListObjectsResponse,
    LockBucketRetentionPolicyRequest,
    NotificationConfig,
    Object,
    ObjectAccessControl,
    ObjectChecksums,
    Owner,
    ProjectTeam,
    QueryWriteStatusRequest,
    QueryWriteStatusResponse,
    ReadObjectRequest,
    ReadObjectResponse,
    RestoreObjectRequest,
    RewriteObjectRequest,
    RewriteResponse,
    ServiceAccount,
    ServiceConstants,
    StartResumableWriteRequest,
    StartResumableWriteResponse,
    UpdateBucketRequest,
    UpdateHmacKeyRequest,
    UpdateObjectRequest,
    WriteObjectRequest,
    WriteObjectResponse,
    WriteObjectSpec,
)

__all__ = (
    "StorageClient",
    "StorageAsyncClient",
    "BidiWriteObjectRequest",
    "BidiWriteObjectResponse",
    "Bucket",
    "BucketAccessControl",
    "CancelResumableWriteRequest",
    "CancelResumableWriteResponse",
    "ChecksummedData",
    "CommonObjectRequestParams",
    "ComposeObjectRequest",
    "ContentRange",
    "CreateBucketRequest",
    "CreateHmacKeyRequest",
    "CreateHmacKeyResponse",
    "CreateNotificationConfigRequest",
    "CustomerEncryption",
    "DeleteBucketRequest",
    "DeleteHmacKeyRequest",
    "DeleteNotificationConfigRequest",
    "DeleteObjectRequest",
    "GetBucketRequest",
    "GetHmacKeyRequest",
    "GetNotificationConfigRequest",
    "GetObjectRequest",
    "GetServiceAccountRequest",
    "HmacKeyMetadata",
    "ListBucketsRequest",
    "ListBucketsResponse",
    "ListHmacKeysRequest",
    "ListHmacKeysResponse",
    "ListNotificationConfigsRequest",
    "ListNotificationConfigsResponse",
    "ListObjectsRequest",
    "ListObjectsResponse",
    "LockBucketRetentionPolicyRequest",
    "NotificationConfig",
    "Object",
    "ObjectAccessControl",
    "ObjectChecksums",
    "Owner",
    "ProjectTeam",
    "QueryWriteStatusRequest",
    "QueryWriteStatusResponse",
    "ReadObjectRequest",
    "ReadObjectResponse",
    "RestoreObjectRequest",
    "RewriteObjectRequest",
    "RewriteResponse",
    "ServiceAccount",
    "ServiceConstants",
    "StartResumableWriteRequest",
    "StartResumableWriteResponse",
    "UpdateBucketRequest",
    "UpdateHmacKeyRequest",
    "UpdateObjectRequest",
    "WriteObjectRequest",
    "WriteObjectResponse",
    "WriteObjectSpec",
)
