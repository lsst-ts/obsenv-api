"""Test fixtures for obsenv-api tests."""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from obsenvapi import main


@pytest_asyncio.fixture
async def app() -> AsyncIterator[FastAPI]:
    """Return a configured test application.

    Wraps the application in a lifespan manager so that startup and shutdown
    events are sent during test execution.
    """
    async with LifespanManager(main.app):
        yield main.app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    """Return an ``httpx.AsyncClient`` configured to talk to the test app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="https://example.com/"
    ) as client:
        yield client
