from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order

class Command(BaseCommand):
    """ Create Order """
    
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.get(username="admin")
        order = Order.objects.get_or_create(
            delivery_address="ul Pupkina d 123 kv 91",
            promocode="SALE123",
            user=user,
        )
        self.stdout.write(f"Order {order} Created!")