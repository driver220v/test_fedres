from . import routes
from .app_logic import find_company_main


@routes.get('/task')
async def upload(request):
    query = request.rel_url.query
    company_name = query['name']
    # key_phrase = query['phrase']

    await find_company_main(company_name)
