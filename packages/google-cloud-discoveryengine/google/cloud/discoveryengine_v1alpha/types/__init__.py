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
from .acl_config import AclConfig
from .acl_config_service import GetAclConfigRequest, UpdateAclConfigRequest
from .chunk import Chunk
from .chunk_service import GetChunkRequest, ListChunksRequest, ListChunksResponse
from .common import (
    CustomAttribute,
    CustomFineTuningSpec,
    DoubleList,
    EmbeddingConfig,
    GuidedSearchSpec,
    IdpConfig,
    IndustryVertical,
    Interval,
    Principal,
    SearchAddOn,
    SearchTier,
    SolutionType,
    UserInfo,
)
from .completion import SuggestionDenyListEntry
from .completion_service import CompleteQueryRequest, CompleteQueryResponse
from .conversation import (
    Conversation,
    ConversationContext,
    ConversationMessage,
    Reply,
    TextInput,
)
from .conversational_search_service import (
    ConverseConversationRequest,
    ConverseConversationResponse,
    CreateConversationRequest,
    DeleteConversationRequest,
    GetConversationRequest,
    ListConversationsRequest,
    ListConversationsResponse,
    UpdateConversationRequest,
)
from .data_store import DataStore
from .data_store_service import (
    CreateDataStoreMetadata,
    CreateDataStoreRequest,
    DeleteDataStoreMetadata,
    DeleteDataStoreRequest,
    GetDataStoreRequest,
    GetDocumentProcessingConfigRequest,
    ListDataStoresRequest,
    ListDataStoresResponse,
    UpdateDataStoreRequest,
    UpdateDocumentProcessingConfigRequest,
)
from .document import Document
from .document_processing_config import DocumentProcessingConfig
from .document_service import (
    CreateDocumentRequest,
    DeleteDocumentRequest,
    GetDocumentRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    UpdateDocumentRequest,
)
from .engine import Engine
from .engine_service import (
    CreateEngineMetadata,
    CreateEngineRequest,
    DeleteEngineMetadata,
    DeleteEngineRequest,
    GetEngineRequest,
    ListEnginesRequest,
    ListEnginesResponse,
    PauseEngineRequest,
    ResumeEngineRequest,
    TuneEngineMetadata,
    TuneEngineRequest,
    TuneEngineResponse,
    UpdateEngineRequest,
)
from .estimate_billing_service import (
    EstimateDataSizeMetadata,
    EstimateDataSizeRequest,
    EstimateDataSizeResponse,
)
from .import_config import (
    BigQuerySource,
    GcsSource,
    ImportDocumentsMetadata,
    ImportDocumentsRequest,
    ImportDocumentsResponse,
    ImportErrorConfig,
    ImportSuggestionDenyListEntriesMetadata,
    ImportSuggestionDenyListEntriesRequest,
    ImportSuggestionDenyListEntriesResponse,
    ImportUserEventsMetadata,
    ImportUserEventsRequest,
    ImportUserEventsResponse,
)
from .purge_config import (
    PurgeDocumentsMetadata,
    PurgeDocumentsRequest,
    PurgeDocumentsResponse,
    PurgeErrorConfig,
    PurgeSuggestionDenyListEntriesMetadata,
    PurgeSuggestionDenyListEntriesRequest,
    PurgeSuggestionDenyListEntriesResponse,
    PurgeUserEventsMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from .recommendation_service import RecommendRequest, RecommendResponse
from .schema import FieldConfig, Schema
from .schema_service import (
    CreateSchemaMetadata,
    CreateSchemaRequest,
    DeleteSchemaMetadata,
    DeleteSchemaRequest,
    GetSchemaRequest,
    ListSchemasRequest,
    ListSchemasResponse,
    UpdateSchemaMetadata,
    UpdateSchemaRequest,
)
from .search_service import SearchRequest, SearchResponse
from .search_tuning_service import (
    TrainCustomModelMetadata,
    TrainCustomModelRequest,
    TrainCustomModelResponse,
)
from .serving_config import ServingConfig
from .serving_config_service import (
    GetServingConfigRequest,
    ListServingConfigsRequest,
    ListServingConfigsResponse,
    UpdateServingConfigRequest,
)
from .site_search_engine import SiteSearchEngine, SiteVerificationInfo, TargetSite
from .site_search_engine_service import (
    BatchCreateTargetSiteMetadata,
    BatchCreateTargetSitesRequest,
    BatchCreateTargetSitesResponse,
    BatchVerifyTargetSitesMetadata,
    BatchVerifyTargetSitesRequest,
    BatchVerifyTargetSitesResponse,
    CreateTargetSiteMetadata,
    CreateTargetSiteRequest,
    DeleteTargetSiteMetadata,
    DeleteTargetSiteRequest,
    DisableAdvancedSiteSearchMetadata,
    DisableAdvancedSiteSearchRequest,
    DisableAdvancedSiteSearchResponse,
    EnableAdvancedSiteSearchMetadata,
    EnableAdvancedSiteSearchRequest,
    EnableAdvancedSiteSearchResponse,
    FetchDomainVerificationStatusRequest,
    FetchDomainVerificationStatusResponse,
    GetSiteSearchEngineRequest,
    GetTargetSiteRequest,
    ListTargetSitesRequest,
    ListTargetSitesResponse,
    RecrawlUrisMetadata,
    RecrawlUrisRequest,
    RecrawlUrisResponse,
    UpdateTargetSiteMetadata,
    UpdateTargetSiteRequest,
)
from .user_event import (
    CompletionInfo,
    DocumentInfo,
    MediaInfo,
    PageInfo,
    PanelInfo,
    SearchInfo,
    TransactionInfo,
    UserEvent,
)
from .user_event_service import CollectUserEventRequest, WriteUserEventRequest

__all__ = (
    "AclConfig",
    "GetAclConfigRequest",
    "UpdateAclConfigRequest",
    "Chunk",
    "GetChunkRequest",
    "ListChunksRequest",
    "ListChunksResponse",
    "CustomAttribute",
    "CustomFineTuningSpec",
    "DoubleList",
    "EmbeddingConfig",
    "GuidedSearchSpec",
    "IdpConfig",
    "Interval",
    "Principal",
    "UserInfo",
    "IndustryVertical",
    "SearchAddOn",
    "SearchTier",
    "SolutionType",
    "SuggestionDenyListEntry",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "Conversation",
    "ConversationContext",
    "ConversationMessage",
    "Reply",
    "TextInput",
    "ConverseConversationRequest",
    "ConverseConversationResponse",
    "CreateConversationRequest",
    "DeleteConversationRequest",
    "GetConversationRequest",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "UpdateConversationRequest",
    "DataStore",
    "CreateDataStoreMetadata",
    "CreateDataStoreRequest",
    "DeleteDataStoreMetadata",
    "DeleteDataStoreRequest",
    "GetDataStoreRequest",
    "GetDocumentProcessingConfigRequest",
    "ListDataStoresRequest",
    "ListDataStoresResponse",
    "UpdateDataStoreRequest",
    "UpdateDocumentProcessingConfigRequest",
    "Document",
    "DocumentProcessingConfig",
    "CreateDocumentRequest",
    "DeleteDocumentRequest",
    "GetDocumentRequest",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "UpdateDocumentRequest",
    "Engine",
    "CreateEngineMetadata",
    "CreateEngineRequest",
    "DeleteEngineMetadata",
    "DeleteEngineRequest",
    "GetEngineRequest",
    "ListEnginesRequest",
    "ListEnginesResponse",
    "PauseEngineRequest",
    "ResumeEngineRequest",
    "TuneEngineMetadata",
    "TuneEngineRequest",
    "TuneEngineResponse",
    "UpdateEngineRequest",
    "EstimateDataSizeMetadata",
    "EstimateDataSizeRequest",
    "EstimateDataSizeResponse",
    "BigQuerySource",
    "GcsSource",
    "ImportDocumentsMetadata",
    "ImportDocumentsRequest",
    "ImportDocumentsResponse",
    "ImportErrorConfig",
    "ImportSuggestionDenyListEntriesMetadata",
    "ImportSuggestionDenyListEntriesRequest",
    "ImportSuggestionDenyListEntriesResponse",
    "ImportUserEventsMetadata",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "PurgeDocumentsMetadata",
    "PurgeDocumentsRequest",
    "PurgeDocumentsResponse",
    "PurgeErrorConfig",
    "PurgeSuggestionDenyListEntriesMetadata",
    "PurgeSuggestionDenyListEntriesRequest",
    "PurgeSuggestionDenyListEntriesResponse",
    "PurgeUserEventsMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "RecommendRequest",
    "RecommendResponse",
    "FieldConfig",
    "Schema",
    "CreateSchemaMetadata",
    "CreateSchemaRequest",
    "DeleteSchemaMetadata",
    "DeleteSchemaRequest",
    "GetSchemaRequest",
    "ListSchemasRequest",
    "ListSchemasResponse",
    "UpdateSchemaMetadata",
    "UpdateSchemaRequest",
    "SearchRequest",
    "SearchResponse",
    "TrainCustomModelMetadata",
    "TrainCustomModelRequest",
    "TrainCustomModelResponse",
    "ServingConfig",
    "GetServingConfigRequest",
    "ListServingConfigsRequest",
    "ListServingConfigsResponse",
    "UpdateServingConfigRequest",
    "SiteSearchEngine",
    "SiteVerificationInfo",
    "TargetSite",
    "BatchCreateTargetSiteMetadata",
    "BatchCreateTargetSitesRequest",
    "BatchCreateTargetSitesResponse",
    "BatchVerifyTargetSitesMetadata",
    "BatchVerifyTargetSitesRequest",
    "BatchVerifyTargetSitesResponse",
    "CreateTargetSiteMetadata",
    "CreateTargetSiteRequest",
    "DeleteTargetSiteMetadata",
    "DeleteTargetSiteRequest",
    "DisableAdvancedSiteSearchMetadata",
    "DisableAdvancedSiteSearchRequest",
    "DisableAdvancedSiteSearchResponse",
    "EnableAdvancedSiteSearchMetadata",
    "EnableAdvancedSiteSearchRequest",
    "EnableAdvancedSiteSearchResponse",
    "FetchDomainVerificationStatusRequest",
    "FetchDomainVerificationStatusResponse",
    "GetSiteSearchEngineRequest",
    "GetTargetSiteRequest",
    "ListTargetSitesRequest",
    "ListTargetSitesResponse",
    "RecrawlUrisMetadata",
    "RecrawlUrisRequest",
    "RecrawlUrisResponse",
    "UpdateTargetSiteMetadata",
    "UpdateTargetSiteRequest",
    "CompletionInfo",
    "DocumentInfo",
    "MediaInfo",
    "PageInfo",
    "PanelInfo",
    "SearchInfo",
    "TransactionInfo",
    "UserEvent",
    "CollectUserEventRequest",
    "WriteUserEventRequest",
)
