import httpx

from src.application.streamer_service import StreamerService
from src.domain.models.streamer import Streamer


class TwitchParser:

    def __init__(self):
        self._client_id = '73cfu3h5frsxq3kqraf21qgy1lki6p'
        self._client_secret = 'sh7d4zosakr1ec4ycan2zisrgmh9pq'
        self._access_token = self._get_auth_token()

    def _get_auth_token(self):
        body = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            "grant_type": 'client_credentials'
        }
        url = 'https://id.twitch.tv/oauth2/token'
        r = httpx.post(url, data=body)

        return r.json()['access_token']

    async def _get_most_popular_channels_info(self):
        url = 'https://api.twitch.tv/helix/streams'
        headers = {
            'Client-ID': self._client_id,
            'Authorization': 'Bearer ' + self._access_token
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        streamers = response.json()['data']
        streamer_model_list = []
        for streamer in streamers:
            streamer_model_list.append(Streamer.parse_obj(streamer))
        return streamer_model_list

    async def parse(self, streamer_service: StreamerService) -> None:
        streamers = await self._get_most_popular_channels_info()
        for streamer in streamers:
            streamer_service.create_streamer(streamer)
