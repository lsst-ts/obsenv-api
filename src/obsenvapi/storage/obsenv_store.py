"""Observatory environment store."""

from __future__ import annotations

from structlog.stdlib import BoundLogger

from obsenvapi.domain.models import PackageInformation

from .store import Store

__all__ = ["ObsenvStore"]


class ObsenvStore(Store):
    """Observatory environment storage handler."""

    def __init__(self, *, logger: BoundLogger) -> None:
        super().__init__(logger=logger)
        self._commander = None

    def get_package_versions(self) -> list[PackageInformation]:
        return [
            PackageInformation(
                name="test", current_version="1.0.0", original_version="1.0.0"
            )
        ]
