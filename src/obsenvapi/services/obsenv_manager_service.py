"""Obsenv Manager Service."""

from __future__ import annotations

from structlog.stdlib import BoundLogger

from ..domain.models import PackageInformation, PackageUpdate
from ..storage.store import Store

__all__ = ["ObsenvManagerService"]


class ObsenvManagerService:
    """A service for managing the obsenv.

    Parameters
    ----------
    logger
        The structlog logger.
    """

    def __init__(self, logger: BoundLogger, obsenv_store: Store) -> None:
        self._logger = logger
        self._obsenv_store = obsenv_store

    def get_package_versions(self, userid: int) -> list[PackageInformation]:
        self._logger.info("Retrive package versions from store.")
        self._logger.info(f"Requested by {userid}")
        return self._obsenv_store.get_package_versions(userid)

    def update_package_version(self, info: PackageUpdate) -> bool:
        mess = [
            f"Updating package {info.name}",
            f"to version {info.version},",
            f"requested by {info.username}",
        ]
        self._logger.info(" ".join(mess))
        return self._obsenv_store.update_package_version(info)
