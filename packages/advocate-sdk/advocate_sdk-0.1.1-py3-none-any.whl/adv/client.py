import os
import requests
import json

from .exceptions import APIException, NoMatchException
from .campaigns import Campaign
from .dctas import DCTA


class AdvClient:
    def __init__(self, api_key, base_url='https://api.adv.gg/v1/'):
        self.api_key = api_key
        self.api_url = os.environ.get('ADVOCATE_API_URL', base_url)

        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('https://', adapter)

        self.dctas = {}

    def _call_advocate_api(self, method, endpoint, data=None, params={}, files=None):
        """
        Low level manager for interfacing with the Advocate API.
        All requests to the API will be handled by this function
        """
        api_call = getattr(self.session, method)
        url = self.api_url + endpoint

        headers = {
            'Authorization': 'API-Key {}'.format(self.api_key),
        }

        kwargs = {}
        if data is not None and files is None:
            kwargs['json'] = data
        elif data is not None:
            kwargs['data'] = {key: json.dumps(value) for key, value in data.items()}
            kwargs['files'] = files

        response = api_call(url, headers=headers, **kwargs)

        if response.status_code >= 200 and response.status_code < 300:
            return response.json() if response.content != b'' else ''
        elif response.status_code >= 400 and response.status_code < 500:
            raise APIException(response.json())
        else:
            raise APIException('Cannot connect to the Advocate API')

    def get(self, endpoint):
        """
        Make a `get` request to the Advocate API
        """
        return self._call_advocate_api('get', endpoint)

    def post(self, endpoint, data, files=None):
        """
        Make a `get` request to the Advocate API
        """
        return self._call_advocate_api('post', endpoint, data=data, files=files)

    def put(self, endpoint, data, files=None):
        """
        Make a `put` request to the Advocate API
        """
        return self._call_advocate_api('put', endpoint, data=data, files=files)

    def patch(self, endpoint, data, files=None):
        """
        Make a `patch` request to the Advocate API
        """
        return self._call_advocate_api('patch', endpoint, data=data, files=files)

    def delete(self, endpoint):
        """
        Make a `delete` request to the Advocate API
        """
        return self._call_advocate_api('delete', endpoint)

    def get_dctas(self):
        """
        Fetches and deserializes all DCTAs from the user's account
        """
        dcta_data = self.get('dctas/')
        dctas = [DCTA.deserialize(self, dcta) for dcta in dcta_data]

        return dctas

    def get_dcta(self, dcta_id):
        """
        Fetchs and deserializes a signle DCTA from the user's account
        """
        dcta_data = self.get('dctas/{}/'.format(dcta_id))
        dcta = DCTA.deserialize(self, dcta_data)

        return dcta

    def get_campaigns(self):
        """
        Fetches and deserializes all Campaigns from the user's account
        """
        campaign_data = self.get('dctas/campaigns/')
        return [Campaign(self, campaign['name'], campaign['slug']) for campaign in campaign_data]

    def get_campaign(self, slug):
        """
        Fetches a single campaign by slug
        """
        campaigns = self.get_campaigns()

        try:
            campaign = next(campaign for campaign in campaigns if campaign.slug == slug)
        except StopIteration:
            raise NoMatchException('Campaign', 'slug', slug)

        return campaign
