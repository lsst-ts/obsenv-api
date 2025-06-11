"""Observatory environment store."""

from __future__ import annotations

from structlog.stdlib import BoundLogger

from ..domain.models import PackageInformation, PackageUpdate, UserInfo
from .obsenv_commander import ObsEnvCommander
from .store import Store

__all__ = ["ObsenvStore"]


class ObsenvStore(Store):
    """Observatory environment storage handler."""

    def __init__(self, *, logger: BoundLogger) -> None:
        super().__init__(logger=logger)
        self._commander = ObsEnvCommander(logger=logger)

    def get_package_versions(
        self, user_info: UserInfo
    ) -> list[PackageInformation]:
        ov, cv = self._commander.get_all_package_versions(user_info)
        return self._parser.parse_double_pass(original=ov, current=cv)

    def update_package_version(self, info: PackageUpdate) -> bool:
        up = self._commander.update_package_version(info)
        return self._parser.parse_update_version(up)
