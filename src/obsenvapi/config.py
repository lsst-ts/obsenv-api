"""Configuration definition."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from safir.logging import LogLevel, Profile

__all__ = ["Config", "config"]


class Config(BaseSettings):
    """Configuration for obsenv-api."""

    name: str = Field("obsenv-api", title="Name of application")

    path_prefix: str = Field("/obsenv-api", title="URL prefix for application")

    profile: Profile = Field(
        Profile.development, title="Application logging profile"
    )

    log_level: LogLevel = Field(
        LogLevel.INFO, title="Log level of the application's logger"
    )

    use_fake_obsenv_manager: bool = Field(
        False,
        title="Use fake manager",
        description=(
            "In place of the real obsenv manager application, use one that"
            " generates fake data."
        ),
    )

    model_config = SettingsConfigDict(
        env_prefix="OBSENV_API_", case_sensitive=False
    )


config = Config()
"""Configuration for obsenv-api."""
