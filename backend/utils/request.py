from typing import Union
import requests

from django.core.cache import cache

from rest_framework.response import Response


def makeRequest(method: str, url: str, data: Union[dict, None] =None):
    if (method, url) in cache:
        return cache.get((method, url))

    result = requests.request(method, url, data=data)
    response = Response(result.content, result.status_code)

    if response.status_code == 200:
        cache.set((method, url), response)
    return response
