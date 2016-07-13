#!/usr/bin/python
#-*-coding:utf-8 -*-

# Copyright 2015 Oktay Sancak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json

API_BASE_URL = 'https://slack.com/api/{api}'

DEFAULT_TIMEOUT = 10

class Error(Exception):
    pass

class Response(object):
    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        self.successful = self.body['ok']
        self.error = self.body.get('error')

class BaseAPI(object):
    def __init__(self, token=None, timeout=DEFAULT_TIMEOUT):
        self.token = token
        self.timeout = timeout

    def _request(self, method, api, **kwargs):
        if self.token:
            kwargs.setdefault('params', {})['token'] = self.token

        response = method(API_BASE_URL.format(api=api),
                          timeout=self.timeout,
                          **kwargs)

        # If made a bad request ( 4xx or 5xx ), will return HTTP status code
        # If status code is 200, will return "None"
        response.raise_for_status()

        response = Response(response.text)
        if not response.successful:
            raise Error(response.error)

        return response

    def post(self, api, **kwargs):
        return self._request(requests.post, api, **kwargs)

class Chat(BaseAPI):
    def post_message(self, channel, text, username=None):
        return self.post('chat.postMessage',
                        data={
                             'channel': channel,
                             'text': text,
                             'username': username
                        })

class Slacker(object):
    def __init__(self, token, incoming_webhook_url=None,
                    timeout=DEFAULT_TIMEOUT):
        self.chat = Chat(token=token, timeout=timeout)
