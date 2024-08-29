"""Models for the obsenv API domain."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["PackageInformation"]


@dataclass(kw_only=True)
class PackageInformation:
    """Clone package information."""

    name: str
    """Name of the cloned package (repository)."""

    current_version: str
    """The version the package is currently checked out to."""

    original_version: str
    """The original version set at a given point."""

    def is_different(self) -> bool:
        return self.current_version != self.original_version
