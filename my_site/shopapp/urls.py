from django.urls import path
from .views import shop_index, groups_list, products_list, orders_list, create_product, create_order


app_name = "shopapp"
# Обращение к ссылками на страницах всегда идет по имени - name
urlpatterns = [
    path("", shop_index, name="index"),
    path('groups/', groups_list, name='groups_list'),
    path('products/', products_list, name='products_list'),
    path('product/new/', create_product, name='create_product'),
    path('orders/', orders_list, name='orders_list'),
    path('order/new/', create_order, name='create_order'),
]