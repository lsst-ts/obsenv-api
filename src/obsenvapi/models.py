"""Models for obsenv-api."""

from typing import Self

from pydantic import BaseModel, Field
from safir.metadata import Metadata as SafirMetadata

from .domain.models import PackageInformation, PackageUpdate

__all__ = [
    "Index",
    "PackageVersions",
    "PackageVersionsResponseModel",
    "SimpleResponseModel",
    "UpdatePackageVersion",
]


class Index(BaseModel):
    """Metadata returned by the external root URL of the application.

    Notes
    -----
    As written, this is not very useful. Add additional metadata that will be
    helpful for a user exploring the application, or replace this model with
    some other model that makes more sense to return from the application API
    root.
    """

    metadata: SafirMetadata = Field(..., title="Package metadata")


class PackageVersions(BaseModel):
    """Package version information."""

    name: str = Field(
        ..., title="Package name", description="Name of the cloned package."
    )
    current_version: str = Field(
        ...,
        title="Current version",
        description="The currently checked out version of a package.",
    )
    original_version: str = Field(
        ...,
        title="Original version",
        description="The original version of the cloned package.",
    )
    is_different: bool = Field(
        False,
        title="Version difference.",
        description=(
            "Flag to highlight is there is a difference between original and "
            "current version."
        ),
    )

    @classmethod
    def from_domain(cls, *, pkg_info: PackageInformation) -> Self:
        """Construct the PackageVersion model from the package information."""
        return cls(
            name=pkg_info.name,
            original_version=pkg_info.original_version,
            current_version=pkg_info.current_version,
            is_different=pkg_info.is_different(),
        )


class PackageVersionsResponseModel(BaseModel):
    """Package version information."""

    fetch_datetime: str = Field(
        ...,
        title="Datetime of fetch",
        description=(
            "The datetime ISO formatted string when the package versions were "
            "fetched."
        ),
    )

    packages: list[PackageVersions] = Field(
        default_factory=list,
        title="Package list",
        description="List of package version information objects.",
    )

    @classmethod
    def from_domain(
        cls, *, fetch_datetime: str, pkg_list: list[PackageInformation]
    ) -> Self:
        """Construct the list of PackageVersions from the information."""
        pkgs = [
            PackageVersions.from_domain(pkg_info=pkg_info)
            for pkg_info in pkg_list
        ]
        return cls(fetch_datetime=fetch_datetime, packages=pkgs)


class SimpleResponseModel(BaseModel):
    "Simple response with just a message."

    msg: str = Field(
        ..., title="Message", description="Message for the response."
    )


class UpdatePackageVersion(BaseModel):
    "Package update information."

    name: str = Field(
        ...,
        title="Package name",
        description="Name of package to update.",
    )

    version: str = Field(
        ...,
        title="Version",
        description="Version to update package to.",
    )

    is_tag: bool = Field(
        False,
        title="Branch/Tag flag",
        description=(
            "A flag to determine if the version is a tag (True) or a branch "
            "(False)."
        ),
    )

    username: str = Field(
        ...,
        title="Username",
        description="Username associated with the update request.",
    )

    userid: str = Field(
        ...,
        title="Userid",
        description="User ID associated with the update request.",
    )

    def to_domain(self) -> PackageUpdate:
        """Construct a PackageUpdate object with the update request
        information.
        """
        return PackageUpdate(
            name=self.name,
            version=self.version,
            is_tag=self.is_tag,
            username=self.username,
            userid=self.userid,
        )
