import logging

import time

import redis
from django.conf import settings
from django.http import HttpRequest, HttpResponseForbidden

url = getattr(settings, 'HTTP_MONITOR_REDIS_URL', 'redis://localhost:6379/0')
url_prefix_list = getattr(settings, 'HTTP_MONITOR_PREFIX_LIST', ['/'])
force_url_list = getattr(settings, 'HTTP_MONITOR_FORCE_URL_LIST', [])
exclude_url_prefix_list = getattr(settings, 'HTTP_MONITOR_EXCLUDE_URL_PREFIX_LIST', ['/http_monitor'])
expire_seconds = getattr(settings, 'HTTP_MONITOR_EXPIRE_SECONDS', 60 * 60 * 24 * 7)

store_prefix = getattr(settings, 'HTTP_MONITOR_STORE_PREFIX', 'http_monitor:')

redis_client = redis.StrictRedis.from_url(url, decode_responses=True)
auth_level = getattr(settings, "HTTP_MONITOR_AUTH_PERMISSION", None)
dynamic_force_url_status = getattr(settings, 'HTTP_MONITOR_DYNAMIC_FORCE_URL_STATUS', False)
force_url_key = 'http_monitor_force_url'


def request_monitor(func):
    def wrapper(*args, **kw):
        from http_monitor.models import Request
        print('request_monitor start')

        request = kw.get('request')

        if not request or not isinstance(request, HttpRequest):
            request = args[0]
        if not request or not isinstance(request, HttpRequest):
            logging.error('no request found for request monitor')
            return

        print('request_monitor %s' % request.build_absolute_uri())
        request._http_request_body = request.body.decode()
        request._start_time = time.time()
        response = func(*args, **kw)
        if hasattr(request, '_start_time'):
            performance = time.time() - request._start_time
            response['API-performance'] = performance
            # request._start_time = None  # when _start_time equal None, there is a error in action retry
        response['Request-UUID'] = Request().add_request(request=request, response=response)

        print('request_monitor end')
        return response

    return wrapper


def auth_permission(func):
    def wrapper(request, *args, **kwargs):
        if auth_level and hasattr(request, 'user'):
            for auth_type in auth_level:
                if getattr(request.user, auth_type):
                    return func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return wrapper

