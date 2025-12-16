"""Streak CRM tap class."""

from __future__ import annotations

from typing import override

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_streakcrm import streams


class TapStreakCRM(Tap):
    """Singer tap for Streak CRM."""

    name = "tap-streakcrm"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,
            description="API key in Streak",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Streak CRM streams.
        """
        return [
            streams.Teams(tap=self),
            streams.Pipelines(tap=self),
            streams.Boxes(tap=self),
        ]
