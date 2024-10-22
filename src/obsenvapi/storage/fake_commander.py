"""Fake commander."""

from __future__ import annotations

import time
from importlib.resources import files

from structlog.stdlib import BoundLogger

from ..config import config
from ..domain.models import PackageUpdate
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
        time.sleep(5)
        cv = (
            files("obsenvapi.data")
            .joinpath("current_versions.out")
            .read_text()
        )
        time.sleep(5)
        return ov, cv

    def update_package_version(self, info: PackageUpdate) -> str:
        if config.use_bad_package_version:
            output_text = (
                files("obsenvapi.data")
                .joinpath("update_package_fail.out")
                .read_text()
            )
        else:
            output_text = (
                files("obsenvapi.data")
                .joinpath("update_package_ok.out")
                .read_text()
            )

        output1 = output_text.replace("<repository>", info.name)
        return output1.replace("<version>", info.version)
