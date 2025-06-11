"""Abstract commander class."""

from __future__ import annotations

from abc import ABC, abstractmethod

from structlog.stdlib import BoundLogger

from ..domain.models import PackageUpdate, UserInfo

__all__ = ["Commander"]


class Commander(ABC):
    """Abstract class for handling manager commands."""

    def __init__(self, *, logger: BoundLogger) -> None:
        self._logger = logger

    @abstractmethod
    def get_all_package_versions(
        self, user_info: UserInfo
    ) -> tuple[str, str]: ...

    @abstractmethod
    def update_package_version(self, info: PackageUpdate) -> str: ...
