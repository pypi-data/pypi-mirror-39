import asyncio
import os
from functools import partial
from pathlib import Path
from typing import FrozenSet, Optional
from uuid import uuid4

import aioredis
import click
import uvloop
from aiohttp import web

from photofinish import utils

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

COOKIE_NAME = os.environ.get("PF_COOKIE_NAME", "PHPSESSIONID")
SESSION_PREFIX = os.environ.get("PF_SESSION_PREFIX", "PHPREDIS_SESSION:")
STORAGE_BASE = os.environ.get("PF_STORAGE_BASE", "/srv")
CLIENT_MAX_SIZE = int(os.environ.get("PF_CLIENT_MAX_SIZE", "10691560"))
REDIS_URL = os.environ.get("PF_REDIS_URL", "redis://127.0.0.1:6379/1")


async def resizer(data: bytes, sizes: FrozenSet[int], extension: str) -> Optional[utils.Images]:
    loop = asyncio.get_event_loop()
    func = partial(utils.resize_image, data, sizes, extension)
    return await loop.run_in_executor(None, func)


async def uploader(request: web.Request):
    session_id = request.cookies.get(COOKIE_NAME)
    if session_id is None:
        raise web.HTTPBadRequest(reason="Empty session")

    try:
        upload_type = utils.UploadType(request.match_info["upload_type"])
    except ValueError:
        raise web.HTTPBadRequest(reason="Unknown format")

    redis: aioredis.Redis = request.app["redis"]
    session: bytes = await redis.get(f"{SESSION_PREFIX}{session_id}")
    user_id = utils.extract_user_id(session)
    if user_id is None:
        raise web.HTTPBadRequest(reason="Broken session")

    body = await request.read()

    base_path = Path(*utils.get_path_chunks(user_id))

    if upload_type in utils.RESIZABLE_TYPES:
        sizes = utils.RESIZABLE_TYPES[upload_type]
        extension = utils.FORCED_EXTENSIONS.get(
            upload_type,
            utils.sniff_extension(body)
        )
        images = await resizer(body, sizes, extension)
        if images is None:
            raise web.HTTPBadRequest(reason="Wrong images")
        paths = {}
        for width, resized_image in images.items():
            name = utils.get_resizable_name(upload_type, width)
            path = (base_path / name).with_suffix(f".{extension}")
            await utils.save_bytes(path, resized_image)
            paths[width] = path.as_posix()
        return web.json_response(paths)
    else:
        name = uuid4().hex
        extension = utils.sniff_extension(body)
        path = (base_path / name).with_suffix(f".{extension}")
        await utils.save_bytes(path, body)
        return web.json_response(path.as_posix())


async def on_shutdown(app):
    await app["redis"].close()
    await app["redis"].wait_closed()


def create_app():
    loop = asyncio.get_event_loop()
    app = web.Application(client_max_size=CLIENT_MAX_SIZE)
    app.router.add_post("/{upload_type}", uploader)
    app["redis"] = loop.run_until_complete(aioredis.create_redis(
        REDIS_URL,
        timeout=5,
        encoding="utf-8"
    ))
    app.on_shutdown.append(on_shutdown)
    return app


@click.command()
def run():
    """Microservice for uploading images and avatars"""
    web.run_app(create_app())
