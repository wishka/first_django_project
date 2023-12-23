from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Avg, Min, Max, Count, Sum

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo addregate")
        # # Добавим агрегатор и фильтр для конкретных товаров(можно без фильтра)
        # result = Product.objects.filter(name__contains='Smartphone').aggregate(
        #     Avg("price"),
        #     Max("price"),
        #     min_price=Min("price"), # Можно добавить именование, чтобы вывод был удобочитаемым
        #     count=Count("id"),
        # )
        #
        # print(result)
        orders = Order.objects.annotate(
            total=Sum('products__price', default=0), # __ Чтобы обратиться к товару,
            # а затем к его цене. Добавим default=0 чтобы извежать в выводе None
            products_count=Count('products'),
        )
        for order in orders:
            print(
                f"Order #{order.id} with {order.products_count} "
                f"products worth {order.total}"
            )
        self.stdout.write("Done")