from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import aiohttp

from src import config



class TrelloWebhookMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            trello_webhook_url: str,
    ):
        super().__init__(app)
        self.trello_webhook_url = trello_webhook_url
        self.payload = {
            "callbackURL": f"{config.APP_URL}/api/trello/webhook",
            "idModel": config.trello.BOARD_ID,
            "key": config.trello.API_KEY,
            "token": config.trello.TOKEN,
            "description": "trello telegram integration"
        }

    async def dispatch(self, request: Request, call_next):
        print('[+] Checking CALLBACK_WEBHOOK_ID')

        if config.trello.CALLBACK_WEBHOOK_ID is None:
            # config trello webhoook
            print(f'[+] CREATING: {self.payload}')

            async with aiohttp.ClientSession() as session:
                async with session.post(self.trello_webhook_url, json=self.payload) as response:
                    result = await response.json()
                    print(f'[+] RESPONSE: {result}')
                    config.trello.CALLBACK_WEBHOOK_ID = result['id']
                    print.info(f'[+] CHECKING GLOBAL: {config.trello.CALLBACK_WEBHOOK_ID}')
        else:
            print(f'[+] Webhook already exists {config.trello.CALLBACK_WEBHOOK_ID}')

        # process the request and get the response    
        response = await call_next(request)

        return response
