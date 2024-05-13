"""Obsenv Manager Service."""

from __future__ import annotations

from structlog.stdlib import BoundLogger

from ..domain.models import PackageInformation
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

    def get_package_versions(self) -> list[PackageInformation]:
        self._logger.info("Retrive package versions from store.")
        return self._obsenv_store.get_package_versions()
