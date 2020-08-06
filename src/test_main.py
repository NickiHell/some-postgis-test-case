import json
from random import randint

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient

import db
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_gis_polygon(async_client: AsyncClient) -> None:
    await db.database.connect()
    response = await async_client.post(
        "/gis_polygon/create?class_id=999&geometry=3 0,6 0,6 3,3 3,3 0",
        json={}
    )
    assert response.status_code == 200
    assert isinstance(json.loads(response.text).get('id'), int)
    await db.database.disconnect()


@pytest.mark.asyncio
async def test_get_gis_polygon(async_client: AsyncClient) -> None:
    await db.database.connect()
    obj = await async_client.post(
        "/gis_polygon/create?class_id=999&geometry=3 0,6 0,6 3,3 3,3 0",
        json={}
    )
    uid = json.loads(obj.text).get('id')
    response = await async_client.get(f"gis_polygon/{uid}")
    assert response.status_code == 200
    assert json.loads(response.text).get('id') == uid
    await db.database.disconnect()


@pytest.mark.asyncio
async def test_delete_gis_polygon(async_client: AsyncClient) -> None:
    await db.database.connect()
    obj = await async_client.post(
        "/gis_polygon/create?class_id=999&geometry=3 0,6 0,6 3,3 3,3 0",
        json={}
    )
    uid = json.loads(obj.text).get('id')
    response = await async_client.delete(f"gis_polygon/{uid}")
    assert response.status_code == 200
    assert json.loads(response.text).get('detail') == "OK"
    await db.database.disconnect()


@pytest.mark.asyncio
async def test_update_gis_polygon(async_client: AsyncClient):
    new_class_id = randint(1, 300)
    await db.database.connect()
    obj = await async_client.post(
        "/gis_polygon/create?class_id=999&geometry=3 0,6 0,6 3,3 3,3 0",
        json={}
    )
    uid = json.loads(obj.text).get('id')
    response = await async_client.patch(
        f"gis_polygon/{uid}?class_id={new_class_id}&"
        f"geometry=3 0,6 0,6 3,3 3,3 0",
        json={}
    )
    assert response.status_code == 200
    response = await async_client.get(f"gis_polygon/{uid}")
    assert response.status_code == 200
    assert int(json.loads(response.text).get('class_id')) == new_class_id
    await db.database.disconnect()
