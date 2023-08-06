from typing import Dict

from aiohttp import web

from .validators import ValidatorError


async def application_json(request: web.Request) -> Dict:
    try:
        resp: Dict = await request.json()
        return resp
    except ValueError as e:
        raise ValidatorError(str(e))
