"""Handle parsing output from obsenv CLI tool."""

from __future__ import annotations

import os

from structlog.stdlib import BoundLogger

from ..domain.models import PackageInformation

__all__ = ["OutputParser"]


class OutputParser:
    """Handle parsing output from obsenv CLI tool."""

    def __init__(self, *, logger: BoundLogger) -> None:
        self._logger = logger

    def parse_double_pass(
        self, original: str, current: str
    ) -> list[PackageInformation]:
        pkg_list = []
        for line in original.strip().split(os.linesep)[2:]:
            if "DEBUG" in line:
                continue
            name_set, original_version = line.strip().split()[-2:]
            name = name_set.rstrip(":")
            pkg_list.append(
                PackageInformation(
                    name=name,
                    original_version=original_version,
                    current_version="",
                )
            )

        for line in current.strip().split(os.linesep)[2:]:
            if "DEBUG" in line:
                continue
            name_set, current_version = line.strip().split()[-2:]
            name = name_set.rstrip(":")
            item = next((i for i in pkg_list if i.name == name), None)
            if item is not None:
                item.current_version = current_version

        return pkg_list

    def parse_update_version(self, output: str) -> bool:
        self._logger.info(f"{'Application error' not in output}")
        return "Application error" not in output
