"""Fake commander."""

from __future__ import annotations

from importlib.resources import files

from structlog.stdlib import BoundLogger

from .commander import Commander

__all__ = ["FakeCommander"]


class FakeCommander(Commander):
    """Handle calls to the fake storage."""

    def __init__(self, *, logger: BoundLogger) -> None:
        super().__init__(logger=logger)

    def get_all_package_versions(self) -> tuple[str, str]:
        ov = (
            files("obsenvapi.data")
            .joinpath("original_versions.out")
            .read_text()
        )
        cv = (
            files("obsenvapi.data")
            .joinpath("current_versions.out")
            .read_text()
        )
        return ov, cv
