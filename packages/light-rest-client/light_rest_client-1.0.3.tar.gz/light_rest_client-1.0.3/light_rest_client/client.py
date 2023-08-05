import requests

from light_rest_client import utils, exceptions
from light_rest_client.parsers import Parser
from light_rest_client.providers import Provider


class Client:
    def __init__(self, url, provider=Provider.empty(), parser=Parser.default()):
        self.url = url
        self.provider = provider
        self.parser = parser

    def get(self, path, payload={}, headers={}):
        if len(headers) == 0:
            headers = self.provider.provide()

        response = requests.get(utils.parse_url(self.url, path), params=payload, headers=headers)
        exceptions.detect_exception(response.status_code)

        return self.parser.parse(response.text)

    def post(self, path, payload={}, headers={}):
        if len(headers) == 0:
            headers = self.provider.provide()

        response = requests.post(utils.parse_url(self.url, path), data=payload, headers=headers)
        exceptions.detect_exception(response.status_code)

        return self.parser.parse(response.text)

    def put(self, path, payload={}, headers={}):
        if len(headers) == 0:
            headers = self.provider.provide()

        response = requests.put(utils.parse_url(self.url, path), data=payload, headers=headers)
        exceptions.detect_exception(response.status_code)

        return self.parser.parse(response.text)

    def delete(self, path, headers={}):
        if len(headers) == 0:
            headers = self.provider.provide()

        response = requests.delete(utils.parse_url(self.url, path), headers=headers)
        exceptions.detect_exception(response.status_code)

        return self.parser.parse(response.text)

    def patch(self, path, payload={}, headers={}):
        if len(headers) == 0:
            headers = self.provider.provide()

        response = requests.patch(utils.parse_url(self.url, path), data=payload, headers=headers)
        exceptions.detect_exception(response.status_code)

        return self.parser.parse(response.text)
