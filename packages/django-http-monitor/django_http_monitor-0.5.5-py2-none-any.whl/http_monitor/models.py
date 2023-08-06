import uuid
from datetime import datetime
import json
import requests

from django.http import HttpResponse

from http_monitor import redis_client, store_prefix, expire_seconds, force_url_key


class Request(object):
    key_base = store_prefix + 'requests:'
    list_key = key_base + 'requests-list'

    def __init__(self, request_id=None):
        self.request_id = request_id if request_id else str(uuid.uuid4())
        item_key_base = self.key_base + self.request_id + ':'
        self.request_key = item_key_base + 'request'
        self.request_headers_key = item_key_base + 'request-headers'
        self.response_key = item_key_base + 'response'
        self.response_headers_key = item_key_base + 'response-headers'
        self.request_user = item_key_base + 'request_user'

    def add_request(self, request, response):
        path = request.get_full_path()

        pipeline = redis_client.pipeline()
        pipeline.rpush(self.list_key, self.request_id)
        pipeline.ltrim(self.list_key, -10000, -1)

        key = self.request_key
        pipeline.hmset(key, {
            'path': path,
            'method': request.method,
            'body': request._http_request_body,
            'host': request.META.get('HTTP_HOST'),
            'status_code': response.status_code,
            'request_id': self.request_id,
            'created_at': datetime.now().isoformat()
        })
        pipeline.expire(key, expire_seconds)

        key = self.request_headers_key
        headers = {key: value for key, value in request.META.items() if key.startswith('HTTP_')}
        pipeline.hmset(key, headers)
        pipeline.expire(key, expire_seconds)

        key = self.response_key
        content = response.content
        pipeline.hmset(key, {
            'status_code': response.status_code,
            'content': content,
            'host': request.META.get('HTTP_HOST'),
        })
        pipeline.expire(key, expire_seconds)

        key = self.response_headers_key
        headers = {key: ', '.join(value) for key, value in response._headers.items()}
        pipeline.hmset(key, headers)
        pipeline.expire(key, expire_seconds)

        key = self.request_user
        user_info = dict()
        if hasattr(request, 'user'):
            user_info = dict(username=request.user.id, id=request.user.username)
        pipeline.hmset(key, user_info)
        pipeline.expire(key, expire_seconds)

        pipeline.execute()

        return self.request_id

    def get_request(self):

        pipeline = redis_client.pipeline()
        key = self.request_key
        pipeline.hgetall(key)

        key = self.request_headers_key
        pipeline.hgetall(key)

        key = self.response_key
        pipeline.hgetall(key)

        key = self.response_headers_key
        pipeline.hgetall(key)

        key = self.request_user
        pipeline.hgetall(key)

        http_request, request_headers, response, response_headers, request_user = pipeline.execute()
        if not http_request:
            return HttpResponse(status=404)

        try:
            content = response.get('content')
            content = json.loads(content)
        except Exception:
            content = 'HTTP monitor json decode error.'

        response['content'] = content

        result = {
            "user": request_user,
            'request': http_request,
            'request_headers': request_headers,
            'response': response,
            'response_headers': response_headers
        }
        return result

    def get_conent(self):
        return redis_client.hget(self.response_key, 'content')

    def get_requests(self, size, page):
        request_ids = redis_client.lrange(self.list_key, -size * page, - ((page - 1) * size + 1))
        request_ids.reverse()
        pipeline = redis_client.pipeline()

        for request_id in request_ids:
            item_key_base = self.key_base + '{requests_id}'.format(requests_id=request_id)
            key = item_key_base + ':request'
            pipeline.hgetall(key)

        return pipeline.execute()

    def retry(self, current_request):
        result = self.get_request()
        request = result.get('request')
        method = request.get('method')
        url = current_request.build_absolute_uri(request.get('path'))
        headers = {k[5:]: v for k, v in result.get('request_headers').items()}
        body = request.get('body')
        r = requests.request(method=method,
                             url=url,
                             data=body,
                             headers=headers)
        return {
            "method": method,
            "url": url,
            "headers": headers,
            "body": body,
            "status_code": r.status_code,
            "content": r.content.decode()
        }


    def get_settings(self):
        apis_count = redis_client.scard(force_url_key)
        apis = redis_client.smembers(force_url_key)

        return {"force_apis_count": apis_count, "force_apis": list(apis)}