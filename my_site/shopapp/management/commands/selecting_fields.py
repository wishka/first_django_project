from typing import Sequence
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """ Create Order with selected fields"""
    # Добавим декоратор, который отслеживает транзакции. Если они не завершены, то откатывает к началу
    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")
        users_info = User.objects.values_list("username", flat=True)
        # flat=True если необходимо сделать список, а не кортеж(только если нужен 1 параметр)
        print(users_info) # - создаст queryset, print(list(users_info)) - вернет список
        for user in users_info:
            print(user)
        # product_values = Product.objects.values("pk", "name")
        # for p_value in product_values:
        #     print(p_value)
        self.stdout.write("Done")