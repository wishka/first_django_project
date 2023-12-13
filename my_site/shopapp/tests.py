from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers


class ProductCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Чтобы использовать созданного пользователя в этом классе тестов, добавим его в словарь
        cls.credentials = dict(username="bob_test", password="querty")
        # Далее распакуем данные
        cls.user = User.objects.create_user(**cls.credentials)
        permission = Permission.objects.get(codename='add_product')
        cls.user.user_permissions.add(permission)
    
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    
    def setUp(self) -> None:
        # Вернем созданного пользователя
        self.client.login(**self.credentials)
        # Сгенерируем случайное название. Для этого используем choices и ascii_letters
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
        
    def test_create_product(self):
        response = self.client.post(
            # Передаем view, на который обращается запрос
            reverse("shopapp:create_product"),
            # А также само тело запроса
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "Bla-bla-bla",
                "discount": "10"
            }
        )
        # Затем проверим ожидаемый результат. В данном случае редирект на страницу продуктов
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


# python manage.py dumpdata shopapp.Product  - данная команда позволяет получить выгрузку
# по всем продуктам в приложении
# python manage.py dumpdata shopapp > shopapp-fixtures.json сохранит все данные в файл
# python manage.py loaddata shopapp-fixtures.json - Позволяет восстановить базу данных из последнего
# сохраненного дампа


class ProductDetailsViewTestCase(TestCase):
    # Необходимо воспользоваться классовыми методами, чтобы быть уверенным, что
    # сущности создаются только 1 раз. classmethod действует по окончанию работы всего теста класса
    # в отличии от простого setUp
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username="".join(choices(ascii_letters, k=10)), password="password")
        cls.product =Product.objects.create(name="".join(choices(ascii_letters, k=10)), created_by=cls.user)
    
    @classmethod
    def tearDownClass(cls): # Выполняется после каждого теста, чтобы очистить БД
        cls.product.delete()
        cls.user.delete()
    
    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)
        
    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Чтобы использовать созданного пользователя в этом классе тестов, добавим его в словарь
        cls.credentials = dict(username="bob_test", password="querty")
        # Далее распакуем данные
        cls.user = User.objects.create_user(**cls.credentials)
    
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    
    def setUp(self):
        # Вернем созданного пользователя
        self.client.login(**self.credentials)
    # Используем фикстуры из дампа продуктов
    fixtures = [
        "products-fixtures.json",
    ]
    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
            # Проверим, что на странице отображаются только не архивированные продукты
        
        # 1-й вариант
        # products = Product.objects.filter(archived=False).all()
        #     # Возьмем продукты из контекста view (context_object_name)
        # products_ = response.context('products')
        #     # Теперь сверим оба списка продуктов. Минус такого подхода только в том,
        #     # что если один список будет меньше, то сравнение будет проходить только по нему
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)
        # 2-й вариант. Еще один вариант пройти по Query-set
        self.assertQuerysetEqual(
            # Сначала передаем список продуктов
            qs=Product.objects.filter(archived=False).all(),
            # Затем то, с чем сравнить
            values=(p.pk for p in response.context['products']),
            # И потом метод transform - для того, чтобы указать, как преобразовывать
            # объекты, чтобы сравнить их с values. qs(query set) будет обработан через transform
            transform=lambda p: p.pk,
        )
        # Так же добавим проверку, какой шаблон был использован
        self.assertTemplateUsed(response, 'shopapp/products-list.html')
        
class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Чтобы использовать созданного пользователя в этом классе тестов, добавим его в словарь
        cls.credentials = dict(username="bob_test", password="querty")
        # Далее распакуем данные
        cls.user = User.objects.create_user(**cls.credentials)
            # Еще один вариант сделать вход пользователя
        # cls.user = User.objects.create_user(username="bob_test", password="querty")
        # Для каждого отдельного теста необходимо делать вход пользователя в методе
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        
    def setUp(self):
        # Вернем созданного пользователя
        self.client.login(**self.credentials)
            # Либо 2-й вариант
        # self.client.force_login(self.user)
    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, 'Orders list')
        
    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        # Так как редирект незалогиненного пользователя идет ленивым методом через LOGIN_URL,
        # необходимо привести к строке данный URL
        self.assertEqual(response.status_code, 302)
            # Эта проверка не пройдет, так как редирект требует внести корректировки
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertIn(str(settings.LOGIN_URL), response.url)
        

class ProductsExportViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Чтобы использовать созданного пользователя в этом классе тестов, добавим его в словарь
        cls.credentials = dict(username="bob_test", password="querty")
        # Далее распакуем данные
        cls.user = User.objects.create_user(**cls.credentials)
        # Еще один вариант сделать вход пользователя
        # cls.user = User.objects.create_user(username="bob_test", password="querty")
        # Для каждого отдельного теста необходимо делать вход пользователя в методе
    
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    
    def setUp(self):
        # Вернем созданного пользователя
        self.client.login(**self.credentials)
    fixtures = [
        "products-fixtures.json",
    ]
    def test_get_products_view(self):
        response = self.client.get(
            reverse('shopapp:products-export')
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )
        

class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="bob_test", password="querty")
        
        # Adding necessary permission to the user
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)
        
    @classmethod
    def tearDownClass(cls):
        # User is cascade deleted, so all the orders will be deleted as well.
        cls.user.delete()
        super().tearDownClass()
    
    def setUp(self):
        self.client.force_login(self.user)
        
        self.order = Order.objects.create(
            user=self.user,
            promocode="777",
            delivery_address="Moscow, Pupkina, d 7, kv 111"
        )
        
        product1 = Product.objects.create(name="Test Product 1", price=100, created_by=self.user)
        product2 = Product.objects.create(name="Test Product 2", price=200, created_by=self.user)
        
        self.order.products.add(product1, product2)
    
    def tearDown(self):
        self.order.delete()
    
    def test_order_details(self):
        # We need to pass the order id to the detail view.
        url = reverse_lazy('shopapp:order_details', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        
        # Check if the correct order is passed to the template context.
        self.assertEqual(response.context['order'].pk, self.order.pk)
        
class OrdersExportTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="bob_test", password="querty")
    
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    
    def setUp(self):
        self.client.force_login(self.user)
        fixtures = [
            "orders-fixtures.json",
        ]
    
    def test_get_orders_view(self):
        response = self.client.get(
            reverse('shopapp:orders-export')
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "user": order.user.username,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data['orders'],
            expected_data,
        )