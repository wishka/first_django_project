from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    class Meta:
        ordering = ["name", "price"] # Сортирует в данном случае по имени и цене
        # db_table = "tech_products" # Позволяет обратиться к базе из которой брать модель
        # verbose_name_plural = "products" # Добавляет отображение модели во множественном числе
        
    name = models.CharField(max_length=32)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    
    @property
    def description_short(self) -> str:
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + "..."
    def __str__(self) -> str:
        return f"Product(pk = {self.pk}), name = {self.name!r}"
    
class Order(models.Model):
    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
