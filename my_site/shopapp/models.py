from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _, ngettext


# Можно сделать функцию, которая будет обрабатывать путь хранения и
# название сохраненного изображения продуктов и добавить ее в параметр 'upload_to'
def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return f"products/product_{instance.pk}/preview/{filename}"


class Product(models.Model):
    """
    Модель Product представляет товар для продажи в интернет-магазине
    Заказы тут :model:`shopapp.Order`
    """
    class Meta:
        ordering = ["name", "price"] # Сортирует в данном случае по имени и цене
        # db_table = "tech_products" # Позволяет обратиться к базе из которой брать модель
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        # verbose_name_plural = "products" # Добавляет отображение модели во множественном числе
        
    name = models.CharField(max_length=32, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)
    
    @property
    def description_short(self) -> str:
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + "..."
    
    def __str__(self) -> str:
        return f"Product(pk = {self.pk}), name = {self.name!r}"


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)
    
    
class Order(models.Model):
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to='orders/receipts/')
