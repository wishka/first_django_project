from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from shopapp.models import Order, Product


class Command(BaseCommand):
    """ Create Order """
    # Добавим декоратор, который отслеживает транзакции. Если они не завершены, то откатывает к началу
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with products")
        user = User.objects.get(username="wishka")
        # products: Sequence[Product] = Product.objects.all()
            # Можно использовать обратный метод от values, и values_list. Нужно быть уверенным,
            # что перечисленные поля действительно не будут использоваться
        # products: Sequence[Product] = Product.objects.defer("description", "price", "created_at").all()
            # Лучше использовать обратный метод от defer - only. Позволяет указать только то, что надо загрузить
        products: Sequence[Product] = Product.objects.only("id", "name").all()
        order, created = Order.objects.get_or_create(
            delivery_address="ul Svetlaya d 123 kv 91",
            promocode="promo1",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Order {order} Created!")