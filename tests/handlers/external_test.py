"""Tests for the obsenvapi.handlers.external module and routes."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from obsenvapi.config import config


@pytest.mark.asyncio
async def test_get_index(client: AsyncClient) -> None:
    """Test ``GET /obsenv-api/``."""
    response = await client.get("/obsenv-api/")
    assert response.status_code == 200
    data = response.json()
    metadata = data["metadata"]
    assert metadata["name"] == config.name
    assert isinstance(metadata["version"], str)
    assert isinstance(metadata["description"], str)
    assert isinstance(metadata["repository_url"], str)
    assert isinstance(metadata["documentation_url"], str)


@pytest.mark.asyncio
async def test_get_package_versions(client: AsyncClient) -> None:
    """Test ``GET /obsenv-api/package_versions/``."""
    config.use_fake_obsenv_manager = True
    user_info = {
        "Obsenv-User-Name": "vera",
        "Obsenv-User-ID": "280723",
    }
    response = await client.get(
        "/obsenv-api/package_versions", headers=user_info
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["packages"]) == 12
    assert isinstance(data["fetch_datetime"], str)


@pytest.mark.asyncio
async def test_update_package_version(client: AsyncClient) -> None:
    """Test ``POST /obsenv-api/update_package_version/``."""
    config.use_fake_obsenv_manager = True
    change_version = {
        "name": "ts_config_ocs",
        "version": "v0.25.6",
        "is_tag": True,
        "username": "vera",
        "userid": "280723",
    }
    response = await client.post(
        "/obsenv-api/update_package", json=change_version
    )
    assert response.status_code == 200
    body = response.json()
    assert body["msg"] == "ts_config_ocs successfully updated"


@pytest.mark.asyncio
async def test_bad_update_package_version(client: AsyncClient) -> None:
    """Test ``POST /obsenv-api/update_package_version/``."""
    config.use_fake_obsenv_manager = True
    config.use_bad_package_version = True
    change_version = {
        "name": "ts_config_ocs",
        "version": "v0.25.6",
        "is_tag": True,
        "username": "vera",
        "userid": "280723",
    }
    response = await client.post(
        "/obsenv-api/update_package", json=change_version
    )
    assert response.status_code == 404
    body = response.json()
    assert (
        body["detail"][0]["msg"]
        == "ts_config_ocs could not be updated. Version v0.25.6 not found"
    )
