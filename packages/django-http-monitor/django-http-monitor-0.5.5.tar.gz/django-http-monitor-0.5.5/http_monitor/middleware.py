import time

from django.conf import settings

from http_monitor import url_prefix_list, exclude_url_prefix_list, force_url_list, redis_client, \
    dynamic_force_url_status, force_url_key
from http_monitor.models import Request
from django.utils.deprecation import MiddlewareMixin


class HttpMonitorMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            request._http_request_body = request.body.decode()
            request._start_time = time.time()
        except Exception:
            pass

    def process_response(self, request, response):
        if not hasattr(request, '_http_request_body'):
            return response

        path = request.path

        if not settings.DEBUG:
            force_url_status = False
            if dynamic_force_url_status:
                force_url_status = redis_client.sismember(force_url_key, path)

            force_url_status = path in force_url_list or force_url_status
            if not force_url_status:
                return response

        if not hasattr(response, 'content'):
            return response

        for url_prefix in url_prefix_list:
            if not path.startswith(url_prefix):
                return response
        for url_prefix in exclude_url_prefix_list:
            if path.startswith(url_prefix):
                return response

        if hasattr(request, '_start_time'):
            performance = time.time() - request._start_time
            response['API-performance'] = performance
            request._start_time = None
        response['Request-UUID'] = Request().add_request(request=request, response=response)
        return response
