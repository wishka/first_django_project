from django.http import HttpRequest, HttpResponseForbidden
import time
from django.conf import settings
from django.core.cache import cache


def set_useragent_on_request_middleware(get_response): # Принимает функцию get_response, которая используется, чтобы получить ответ(выполнить обработку запроса)
    """ Функция для установки User-Agent на запрос"""
    print('Initial call') # Происходит при старте приложения
    def middleware(request: HttpRequest):
        print('Before get response')
        request.user_agent = request.META.get('HTTP_USER_AGENT', '')
        response = get_response(request)
        print('After get response')
        return response
    return middleware

# Сделаем класс для хранения счетчиков посещения страниц.
class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0 # Счетчик запросов страниц
        self.responses_count = 0 # Счетчик ответов страниц
        self.exceptions_count = 0 # Счетчик ошибок страниц
        
    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests_count:', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses_count:', self.responses_count)
        return response
    
    # Функция для обработки ошибок во views.py
    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('Total exceptions:', self.exceptions_count)
        # Можно обрабатывать исключения а также те ответы, которые не должен видеть пользователю
        # а вместо них возвращать какое-нибудь стандартное значение


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        http_request = self.create_http_request(request)
        ip_address = self.get_client_ip(http_request)
        if self.is_request_throttled(ip_address):
            return HttpResponseForbidden("Too many requests. Please try again later.")

        response = self.get_response(http_request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def create_http_request(self, request_dict):
        http_request = HttpRequest()
        for key, value in request_dict.items():
            setattr(http_request, key, value)
        return http_request

    def is_request_throttled(self, ip_address):
        last_request_time = self.get_last_request_time(ip_address)
        current_time = time.time()
        elapsed_time = current_time - last_request_time

        if elapsed_time < settings.REQUEST_THROTTLE_TIME:
            return True

        self.update_last_request_time(ip_address, current_time)
        return False

    def get_last_request_time(self, ip_address):
        last_request_time = cache.get(ip_address)
        return last_request_time or 0

    def update_last_request_time(self, ip_address, current_time):
        cache.set(ip_address, current_time, settings.REQUEST_THROTTLE_TIME)