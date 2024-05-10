"""Fake Obsenv Store."""

from __future__ import annotations

from structlog.stdlib import BoundLogger

from ..domain.models import PackageInformation
from .fake_commander import FakeCommander
from .output_parser import OutputParser

__all__ = ["FakeObsenvStore"]


class FakeObsenvStore:
    """Handle creating information from fake data."""

    def __init__(self, logger: BoundLogger) -> None:
        self._logger = logger
        self._parser = OutputParser(logger=logger)
        self._commander = FakeCommander(logger=logger)

    def get_package_versions(self) -> list[PackageInformation]:
        fake_ov, fake_cv = self._commander.get_all_package_versions()
        return self._parser.parse_double_pass(
            original=fake_ov, current=fake_cv
        )
