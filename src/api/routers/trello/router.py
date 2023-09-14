from fastapi import APIRouter, Request, HTTPException

from . import utils, services



router = APIRouter(
    prefix='/trello',
    tags=['Trello']
)


@router.post('/webhook')
async def handle_trello_webhook(request: Request):
    payload = await request.body()

    kwargs = {'payload': payload}

    print(payload)

    return 'ok'

    # return await services.Trello.handle_webhook(**kwargs)


@router.head('/webhook')
async def hook_trello_webhook():
    return 'OK'
