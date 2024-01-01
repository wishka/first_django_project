from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv_products
from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through # Покажет, с какими заказами связан продукт


class ProductInline(admin.StackedInline):
    model = ProductImage
    

@admin.action(description="Mark archived")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    return queryset.update(archived=True)


@admin.action(description="Unarchived")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    return queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products_changelist.html"
    actions = [
        mark_archived,
        mark_unarchived,
        "export_as_csv"
    ]
    inlines = [
        OrderInline, ProductInline
    ]
    list_display = ("pk", "name", "description_short", "price", "discount", "archived")
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
        }),
        ("Images", {
            "fields": ("preview",),
        })
    ]
    
    # Можно сделать так, если метод description_short будет использоваться в админке
    # def description_short(self, obj: Product):
    #     if len(obj.description) < 48:
    #         return obj.description
    #     return obj.description[:48] + "..."
    
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)
        save_csv_products(
            file=form.files["csv_file"].file,
            encoding=request.encoding
        )
        
        self.message_user(request, "Data from CSV was imported!")
        return redirect("..")
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            )
        ]
        return new_urls + urls


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
