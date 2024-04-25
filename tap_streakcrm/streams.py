"""Stream type classes for tap-streakcrm."""

from __future__ import annotations

from singer_sdk import typing as th

from tap_streakcrm.client import StreakCRMStream


class Teams(StreakCRMStream):
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
    ).to_dict()
