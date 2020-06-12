from aiohttp import web


from .app_init import create_app

fed_res = 'https://fedresurs.ru/search/entity?name'
routes = web.RouteTableDef()

from . import app_routes