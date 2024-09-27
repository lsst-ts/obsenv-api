"""Observatory environment store."""

from __future__ import annotations

from structlog.stdlib import BoundLogger

from ..domain.models import PackageInformation
from .obsenv_commander import ObsEnvCommander
from .store import Store

__all__ = ["ObsenvStore"]


class ObsenvStore(Store):
    """Observatory environment storage handler."""

    def __init__(self, *, logger: BoundLogger) -> None:
        super().__init__(logger=logger)
        self._commander = ObsEnvCommander(logger=logger)

    def get_package_versions(self) -> list[PackageInformation]:
        ov, cv = self._commander.get_all_package_versions()
        return self._parser.parse_double_pass(original=ov, current=cv)
