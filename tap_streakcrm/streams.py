"""Stream type classes for tap-streakcrm."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, override

from requests.auth import HTTPBasicAuth
from singer_sdk import RESTStream
from singer_sdk import typing as th
from singer_sdk.pagination import BasePageNumberPaginator

if TYPE_CHECKING:
    from collections.abc import Iterable

    from singer_sdk.helpers.types import Context, Record


_T = TypeVar("_T")


class StreakCRMStream(RESTStream[_T]):
    """Streak CRM stream class."""

    url_base = "https://api.streak.com/api"

    @override
    @property
    def authenticator(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.config["api_key"], "")

    @override
    def get_url_params(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {}


class Teams(StreakCRMStream[Any]):
    """Teams stream."""

    name = "teams"
    path = "/v2/users/me/teams"
    primary_keys = ("key",)
    records_jsonpath = "$.results[*]"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("creationDate", th.IntegerType),
        th.Property("creator", th.StringType),
        th.Property(
            "members",
            th.ArrayType(
                th.ObjectType(
                    th.Property("role", th.StringType),
                    th.Property("inviteDate", th.IntegerType),
                    th.Property("inviteStatus", th.StringType),
                    th.Property("orgKey", th.StringType),
                    th.Property("emailSharing", th.BooleanType),
                    th.Property("displayName", th.StringType),
                    th.Property("email", th.StringType),
                    th.Property("fullName", th.StringType),
                    th.Property("givenName", th.StringType),
                    th.Property("image", th.StringType),
                    th.Property("userKey", th.StringType),
                ),
            ),
        ),
        th.Property("name", th.StringType),
        th.Property("sharingRestrictedToTeam", th.BooleanType),
        th.Property("automaticallyApproveJoinRequests", th.BooleanType),
        th.Property("key", th.StringType),
        th.Property(
            "billingInfo",
            th.ObjectType(
                th.Property("eligibleForTrial", th.BooleanType),
                th.Property("eligibleForProPlusTrial", th.BooleanType),
                th.Property("manualSettlement", th.BooleanType),
                th.Property("billingScope", th.StringType),
            ),
        ),
        th.Property("hasStripeCustomer", th.BooleanType),
        th.Property("lastSavedTimestamp", th.IntegerType),
        th.Property(
            "contactOrgListPermissions",
            th.ObjectType(
                additional_properties=th.ObjectType(
                    th.Property("aclEntries", th.ArrayType(th.ObjectType())),
                ),
            ),
        ),
    ).to_dict()


class Pipelines(StreakCRMStream[Any]):
    """Pipelines stream."""

    name = "pipelines"
    path = "/v1/pipelines"
    primary_keys = ("key",)
    records_jsonpath = "$[*]"
    replication_key = None

    schema = th.PropertiesList(
        th.Property(
            "creatorKey",
            th.StringType,
            description="The user key of the user that created the pipeline",
        ),
        th.Property("name", th.StringType, description="The name of this pipeline"),
        th.Property(
            "teamWide",
            th.BooleanType,
            description="Whether this pipeline is shared with all users in the organization (same domain in email address)",  # noqa: E501
        ),
        th.Property(
            "fields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("key", th.StringType),
                    th.Property("type", th.StringType),
                )
            ),
            description="Describes what fields each box within the pipeline can have",
        ),
        th.Property(
            "stages",
            th.ObjectType(
                additional_properties=th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("key", th.StringType),
                ),
            ),
            description="A map describing the set of possible stages a box within the pipeline can be in",  # noqa: E501
        ),
        th.Property(
            "stageOrder",
            th.ArrayType(th.StringType),
            description="Editable array which allows you to reorder the stages. This modifies the order of the stages that appear in the web UI.",  # noqa: E501
        ),
        th.Property("creationTimestamp", th.IntegerType),
        th.Property("lastUpdatedTimestamp", th.IntegerType),
        th.Property(
            "aclEntries",
            th.ArrayType(
                th.ObjectType(
                    th.Property("fullName", th.StringType),
                    th.Property("email", th.StringType),
                    th.Property("isOwner", th.BooleanType),
                    th.Property("image", th.StringType),
                )
            ),
            description="An array of ACL objects (with properties: fullName, email, isOwner, image) which determines a list of users who have access to this pipeline.",  # noqa: E501
        ),
        th.Property("pipelineKey", th.StringType),
        th.Property(
            "owner",
            th.ObjectType(
                th.Property("email", th.StringType),
                th.Property("isOwner", th.BooleanType),
            ),
        ),
        th.Property("key", th.StringType),
    ).to_dict()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: Any | None = None,
    ) -> dict[str, Any]:
        """Get URL parameters for the stream."""
        params = super().get_url_params(context, next_page_token)
        params["sortBy"] = "lastUpdatedTime"
        return params

    @override
    def generate_child_contexts(
        self,
        record: Record,
        context: Context | None = None,
    ) -> Iterable[Context | None]:
        """Generate child contexts for each record."""
        yield {"pipelineKey": record["pipelineKey"]}


class Boxes(StreakCRMStream[int]):
    """Boxes stream."""

    name = "boxes"
    path = "/v1/pipelines/{pipelineKey}/boxes"
    primary_keys = ("key",)
    records_jsonpath = "$[*]"
    replication_key = None

    _page_size = 100

    parent_stream_type = Pipelines

    schema = th.PropertiesList(
        th.Property("pipelineKey", th.StringType),
        th.Property("creatorKey", th.StringType),
        th.Property("creationTimestamp", th.IntegerType),
        th.Property("lastUpdatedTimestamp", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("notes", th.StringType),
        th.Property("stageKey", th.StringType),
        th.Property("fields", th.ObjectType()),
        th.Property("followerKeys", th.ArrayType(th.StringType)),
        th.Property("followerCount", th.IntegerType),
        th.Property("commentCount", th.IntegerType),
        th.Property("taskTotal", th.IntegerType),
        th.Property("gmailThreadCount", th.IntegerType),
        th.Property("fileCount", th.IntegerType),
        th.Property("boxKey", th.StringType),
        th.Property("key", th.StringType),
    ).to_dict()

    @override
    def get_new_paginator(self) -> BasePageNumberPaginator | None:
        # Pages are 0 indexed
        return BasePageNumberPaginator(start_value=0)

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None = None,
    ) -> dict[str, Any]:
        """Get URL parameters for the stream."""
        params = super().get_url_params(context, next_page_token)
        params.update(
            {
                "limit": self._page_size,
                "sortBy": "lastUpdatedTime",
            },
        )
        if next_page_token is not None:
            params["page"] = next_page_token
        return params

    @override
    def generate_child_contexts(
        self,
        record: Record,
        context: Context | None = None,
    ) -> Iterable[Context | None]:
        yield {"boxKey": record["boxKey"]}
