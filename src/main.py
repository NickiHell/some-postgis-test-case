import logging
from typing import Dict

from asyncpg import InternalServerError
from fastapi import FastAPI, HTTPException
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from pyproj import Transformer, Proj
from shapely.ops import transform

import db

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.database.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.database.disconnect()


@app.post('/gis_polygon/create', tags=['GIS Polygon'])
async def create_gis_polygon(class_id: str, props: Dict, geometry: str):
    """
    Эндпоинт для создания записи gis_polygon
    :param class_id: id класса
    :param props: JSON с props
    :param geometry: Строка с EPSG:4326 координатами (6 величин)
    :return: id или ошибка
    """
    query = db.gis_polygon.insert().values(
        class_id=class_id,
        props=props,
        geometry=WKTElement(f'POLYGON(({geometry}))', srid=4326)
    )
    try:
        result = await db.database.execute(query)
    except InternalServerError as err:
        logging.log(logging.ERROR, err)
        raise HTTPException(status_code=400, detail=f'{err.message}')
    return {'id': result}


@app.get('/gis_polygon/{polygon_id}', tags=['GIS Polygon'])
async def get_gis_polygon(polygon_id: int):
    """
    Эндпоинт для получения записи gis_polygon по id
    :param polygon_id: id записи
    :return: Сериализованная запись
    """
    query = db.gis_polygon.select().where(
        db.gis_polygon.c.id == polygon_id
    )
    try:
        result = await db.database.fetch_one(query)
    except Exception as exc:
        logging.log(logging.ERROR, exc)
        raise exc
    if not result:
        raise HTTPException(status_code=404, detail="GIS Polygon not found")
    ewkt_geom = to_shape(result.get('geometry'))
    transformer = Transformer.from_proj(
        Proj('epsg:4326'),
        Proj('epsg:32644'))
    geometry = transform(transformer.transform, ewkt_geom)
    result = dict(result)
    result.update({'geometry': str(geometry)[10:-2]})
    return result


@app.delete('/gis_polygon/{polygon_id}', tags=['GIS Polygon'])
async def delete_gis_polygon(polygon_id: int):
    """
    Эндпоинт для удаления gis_polygon по id\n
    :param polygon_id: id записи\n
    :return: OK, 404 или ошибка\n
    """
    query = db.gis_polygon.delete().where(
        db.gis_polygon.c.id == polygon_id
    )
    try:
        result = await db.database.execute(query)
    except Exception as exc:
        logging.log(logging.ERROR, exc)
        raise exc
    return {'detail': 'OK' if not result else str(result)}


@app.patch('/gis_polygon/{polygon_id}', tags=['GIS Polygon'])
async def update_gis_polygon(polygon_id: int, class_id: str, props: Dict,
                             geometry: str):
    """
    Эндпоинт для редактирования записи gis_polygon
    :param polygon_id: id записи
    :param class_id: id класса
    :param props: ???
    :param geometry: Геометрия
    :return: OK или ошибка
    """
    query = db.gis_polygon.update().where(
        db.gis_polygon.c.id == polygon_id
    ).values(
        class_id=class_id,
        props=props,
        geometry=WKTElement(f'POLYGON(({geometry}))', srid=4326)
    )
    try:
        result = await db.database.execute(query)
    except InternalServerError as err:
        logging.log(logging.ERROR, err)
        raise HTTPException(status_code=400, detail=f'{err.message}')
    return {'detail': 'OK' if not result else str(result)}
