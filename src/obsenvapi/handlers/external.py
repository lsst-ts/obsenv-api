"""Handlers for the app's external root, ``/obsenv-api/``."""

import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from safir.dependencies.logger import logger_dependency
from safir.metadata import get_metadata
from safir.models import ErrorDetail, ErrorLocation, ErrorModel
from structlog.stdlib import BoundLogger

from ..config import config
from ..factory import Factory
from ..models import (
    Index,
    PackageVersionsResponseModel,
    SimpleResponseModel,
    UpdatePackageVersion,
)

__all__ = ["external_router", "get_index"]

external_router = APIRouter()
"""FastAPI router for all external handlers."""


@external_router.get(
    "/",
    description=(
        "Document the top-level API here. By default it only returns metadata"
        " about the application."
    ),
    response_model_exclude_none=True,
    summary="Application metadata",
)
async def get_index(
    logger: Annotated[BoundLogger, Depends(logger_dependency)],
) -> Index:
    """GET ``/obsenv-api/`` (the app's external root).

    Customize this handler to return whatever the top-level resource of your
    application should return. For example, consider listing key API URLs.
    When doing so, also change or customize the response model in
    `obsenvapi.models.Index`.

    By convention, the root of the external API includes a field called
    ``metadata`` that provides the same Safir-generated metadata as the
    internal root endpoint.
    """
    # There is no need to log simple requests since uvicorn will do this
    # automatically, but this is included as an example of how to use the
    # logger for more complex logging.
    logger.info("Request for application metadata")

    metadata = get_metadata(
        package_name="obsenv-api",
        application_name=config.name,
    )
    return Index(metadata=metadata)


@external_router.get(
    "/package_versions",
    description="Get all the versions of the cloned packages.",
    summary="Package versions",
)
async def package_versions(
    logger: Annotated[BoundLogger, Depends(logger_dependency)],
    request: Request,
) -> PackageVersionsResponseModel:
    """GET `/obsenv-api/package_versions` endpoint."""
    factory = Factory(logger=logger)
    service = factory.create_obsenv_manager_service()
    username = request.headers.get("Obsenv-User-Name")
    if username is None:
        username = "nouser"
    pkg_list = service.get_package_versions(username)
    fetch_datetime = datetime.datetime.now(datetime.UTC).isoformat()
    return PackageVersionsResponseModel.from_domain(
        fetch_datetime=fetch_datetime, pkg_list=pkg_list
    )


@external_router.post(
    "/update_package",
    description="Update a package to the requested version.",
    summary="Update package version",
    responses={
        404: {"description": "Version not found.", "model": ErrorModel}
    },
)
async def update_package(
    logger: Annotated[BoundLogger, Depends(logger_dependency)],
    update_info: UpdatePackageVersion,
) -> SimpleResponseModel:
    """POST `/obsenv-api/update_package` endpoint."""
    factory = Factory(logger=logger)
    service = factory.create_obsenv_manager_service()
    was_updated = service.update_package_version(update_info.to_domain())
    if was_updated:
        message = f"{update_info.name} successfully updated"
    else:
        message = (
            f"{update_info.name} could not be updated. Version "
            f"{update_info.version} not found"
        )
        error = ErrorDetail(
            loc=[ErrorLocation.body, "version"],
            msg=message,
            type="unknown_version",
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[error.model_dump(exclude_none=True)],
        )

    return SimpleResponseModel(msg=message)
