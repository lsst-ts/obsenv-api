"""Models for the obsenv API domain."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["PackageInformation", "PackageUpdate"]


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


@dataclass(kw_only=True)
class PackageUpdate:
    """Package update information."""

    name: str
    """Name of the package to update."""

    version: str
    """The version to update the package to."""

    is_tag: bool
    """Flag to determine if version is a tag (True) or a branch (False)."""

    username: str
    """"The username associated with the package update request."""
