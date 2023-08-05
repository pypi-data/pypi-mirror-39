import json

import requests

from .models.incoming import Request, Types
from .models.messages import Message
from .models.settings import Analytics


class FacebookClient:
    def __init__(self, page_token: str = None, timeout=5, version=2.6):
        if not isinstance(page_token, str):
            raise TypeError("page_token must be an instance of str")
        self.page_token = page_token
        self.text_message_processor = None
        self.postback_processor = None
        self.fb_url = f'https://graph.facebook.com/v{version}/me/{"{}"}?access_token={page_token}'
        self.timeout = timeout

    def register_text_message_processor(self):
        def add(processor):
            self.text_message_processor = processor
            return processor

        return add

    def register_postback_processor(self):
        def add(processor):
            self.postback_processor = processor
            return processor

        return add

    def process_json(self, msg_json: dict):
        if not isinstance(msg_json, dict):
            raise TypeError('msg_json must be an instance of dict')
        if 'entry' not in msg_json:
            raise ValueError("Malformed incoming request from Facebook")
        request = Request(**msg_json)
        message = request.entries[0].message
        if message.type == Types.TEXT_MESSAGE:
            if not self.text_message_processor:
                raise AttributeError('text_message_processor not declared')
            self.text_message_processor(message)
        elif message.type == Types.POSTBACK_MESSAGE:
            if not self.postback_processor:
                raise AttributeError('postback_processor not declared')
            self.postback_processor(message)
        else:
            raise ValueError("Unknown message type")
        return

    def send_message(self, recipient_id: int, message: Message):
        if not isinstance(message, Message):
            raise TypeError('message must be an instance of Message')
        if not isinstance(recipient_id, int):
            raise TypeError('recipient_id must be an instance of int')
        resp = self.post_request('messages',
                                 json.dumps({'message': message.to_dict(), 'recipient': {'id': recipient_id}}))
        return resp

    def set_whitelist(self, domains: list):
        if not isinstance(domains, list):
            raise TypeError('domains must be an instance of list')
        return self.post_request('messenger_profile', json.dumps({'whitelisted_domains': domains}))

    def set_persistent_menu(self, menus: list, get_started_payload: str = 'get_started'):
        if not isinstance(menus, list):
            raise TypeError('menus must be an instance of list')
        return self.post_request('messenger_profile',
                                 json.dumps({'persistent_menu': [menu.to_dict() for menu in menus],
                                             "get_started": {"payload": get_started_payload}}))

    def post_request(self, endpoint: str, data: str):
        if not isinstance(endpoint, str):
            raise TypeError('endpoint must be an instance of str')
        if not isinstance(data, str):
            raise TypeError('data must be an instance of str')
        headers = requests.utils.default_headers()
        headers['Content-Type'] = 'application/json'
        response = requests.post(self.fb_url.format(endpoint), data=data, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return json.loads(response.text)

    def send_analytics(self, analytics: Analytics, app_id):
        headers = requests.utils.default_headers()
        headers['Content-Type'] = 'application/json'
        response = requests.post(f'https://graph.facebook.com/{app_id}/activities',
                                 data=json.dumps(analytics.to_dict()), headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return json.loads(response.text)
