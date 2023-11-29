from django.http import HttpRequest
import time
from django.shortcuts import render


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
        self.request_vists = {}
        self.time_delay = 10

    def __call__(self, request: HttpRequest):
        request_ip = request.META.get('REMOTE_ADDR')
        request_url = request.build_absolute_uri()
        request_time = round(time.time())

        if request_ip in self.request_vists and request_url == self.request_vists[request_ip][1]:
            past_time = round(time.time()) - self.request_vists[request_ip][0]
            if past_time < self.time_delay:
                context = {
                    'time_left': self.time_delay - past_time,
                    'time': self.time_delay
                }
                return render(request, 'requestdataapp/trottling-error.html', context=context)

        self.request_vists[request_ip] = [request_time, request_url]
        response = self.get_response(request)
        return response