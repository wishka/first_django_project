from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ShopIndexView, GroupsListView,
                    OrdersListView, OrderDetailView,
                    OrderCreateView, ProductCreateView,
                    ProductDetailsView, ProductsListView,
                    ProductUpdateView, ProductDeleteView,
                    OrderUpdateView, OrderDeleteView,
                    ProductsDataExportView, OrdersDataExportView,
                    ProductViewSet, OrdersViewSet, LatestProductFeed,
                    UserOrdersListView, UserOrdersDataExportView,
                    )
from django.views.decorators.cache import cache_page


app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrdersViewSet)

# Обращение к ссылками на страницах всегда идет по имени - name
urlpatterns = [
    # Добавим декоратор на класс ShopIndexView, чтобы кешировать класс
    path("", cache_page(60 * 3)(ShopIndexView.as_view()), name="index"),
    path("api/", include(routers.urls)),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/export/', ProductsDataExportView.as_view(), name='products-export'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/new/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive', ProductDeleteView.as_view(), name='product_delete'),
    path('products/latest/feed/', LatestProductFeed(), name='products-feed'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/export/', OrdersDataExportView.as_view(), name='orders-export'),
    path('order/new/', OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name='user_orders'),
    path('users/<int:user_id>/orders/export/', UserOrdersDataExportView.as_view(), name='user-orders-export'),
    
]