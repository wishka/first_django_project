from django.urls import path
from .views import (ShopIndexView, GroupsListView,
                    OrdersListView, OrderDetailView,
                    OrderCreateView, ProductCreateView,
                    ProductDetailsView, ProductsListView,
                    ProductUpdateView, ProductDeleteView,
                    OrderUpdateView, OrderDeleteView
                    )


app_name = "shopapp"
# Обращение к ссылками на страницах всегда идет по имени - name
urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/new/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('order/new/', OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
]