import typing

from aiohttp import web

from .validators import ValidatorError


async def application_json(request: web.Request) -> typing.Dict:
    try:
        return await request.json()
    except ValueError as e:
        raise ValidatorError(str(e))
