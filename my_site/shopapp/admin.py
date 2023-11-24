from django.contrib import admin

from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through # Покажет, с какими заказами связан продукт
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,
    ]
    list_display = ("pk", "name", "description_short", "price", "discount")
    list_display_links = ("pk", "name")
    ordering = "pk", # Позволяет сортировать по первичному ключу. , в конце обязательна так как
    # сортировка требует кортеж. Если требуется сортировка по имени и цене то , не нужна
    search_fields = "name", "description"
    fieldsets = [
        # None - имя неименованной секции
        (None, {
            "fields": ("name", "description")
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse",),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("wide", "collapse",),
            "description": "Extra options. Field 'archived' is a soft delete field."
        })
    ]
    
    # Можно сделать так, если метод description_short будет использоваться в админке
    # def description_short(self, obj: Product):
    #     if len(obj.description) < 48:
    #         return obj.description
    #     return obj.description[:48] + "..."
class ProductInline(admin.TabularInline): # можно использовать StackedInline. Меняет только вид в админке
    model = Order.products.through # Достает все продукты, связанные с заказом

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose_name"
    
    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")
    
    def user_verbose_name(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
