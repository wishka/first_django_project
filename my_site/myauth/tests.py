from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
# Используем reverse чтобы не указывать прямые ссылки

class GetCookieViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
    def test_get_cookie_view(self):
        response = self.client.get(reverse("myauth:cookie-get"), user=self.user)
        # client - позволяет выполнять имитированные запросы к приложению и проверять ответы
        # Используем get для отправки get-запроса
        # self.assertRedirects(response, '/accounts/login/?next=/accounts/cookie/get')
        self.assertContains(response, "Cookie value")
    
    def tearDown(self):
        self.user.delete()
        

class FooBarViewTest(TestCase):
    def test_foo_bar_view(self ):
        response = self.client.get(reverse("myauth:foo-bar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            # Проверим заголовки ожидая Json
            response.headers['content-type'], 'application/json'
        )
        expected_data = {"foo": "bar", "spam": "eggs"}
        # received_data = json.loads(response.content) # Приведем полученный ответ к json
        # # Сравним полученный результат
        # self.assertEqual(received_data, expected_data)
        self.assertJSONEqual(response.content, expected_data) # В django для приведения к
        # Json есть assertJSONEqual, поэтому лишний код можно брать
