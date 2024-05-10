"""Component factory for the application."""

from structlog.stdlib import BoundLogger

from .config import config
from .services.obsenv_manager_service import ObsenvManagerService
from .storage.fake_obsenv_store import FakeObsenvStore


class Factory:
    """A factory for the application components."""

    def __init__(self, *, logger: BoundLogger) -> None:
        self.logger = logger

    def create_obsenv_manager_service(self) -> ObsenvManagerService:
        """Create an obsenv manager service."""
        return ObsenvManagerService(
            logger=self.logger, obsenv_store=self.create_obsenv_store()
        )

    def create_obsenv_store(self) -> FakeObsenvStore | None:
        """Create an observer store."""
        if config.use_fake_obsenv_manager:
            return FakeObsenvStore(logger=self.logger)
        else:
            return None
