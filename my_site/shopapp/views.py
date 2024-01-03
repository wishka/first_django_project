"""
В этом модуле лежат наборы представлений
"""
from csv import DictWriter
import logging
from timeit import default_timer

from django.contrib.syndication.views import Feed
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import GroupForm, ProductForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer
from .common import save_csv_products
from drf_spectacular.utils import extend_schema, OpenApiResponse


# Это стандартный формат создания нового логгера
log = logging.getLogger(__name__)


# ModelViewSet - используется для rest api. Возвращается ответ в json, который
# необходим для взаимодействия различных api между собой
@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Если не указать фильтр, будет использоваться тот, который стоит по умолчанию
    # Укажем другой фильтр
    filter_backends = [
        SearchFilter,
        # добавим фильтр по умолчанию, чтобы можно было искать по полному совпадению
        DjangoFilterBackend,
        OrderingFilter # Фильтр для сортировки
    ]
    search_fields = ["name", "description"]
    filterset_fields = ["name", "description", "price", "discount", "archived"]
    ordering_fields = ["name", "price", "discount"]
    
    @extend_schema(
        # Короткая информация об этом view
        summary="Get 1 product by id",
        description="Retrieve **product**, return 404 if not found",
        responses= {
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response. Product not found"),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
    
    @action(methods=["get"], detail=False) #Если указать true, то будет построена ссылка с учетом PK
    def download_csv(self, request: Request):
        response: HttpResponse = HttpResponse(content_type='text/csv')
        filename = "products-export.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name", "description", "price", "discount"
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()
        
        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        
        return response
    
    @action(detail=False, methods=["post"], parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Dasktop', 3004),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        # Необходимо указать параметры форматирования
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        print('shop index context', context)
        return render(request, 'shopapp/shop-index.html', context=context)
    

class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all()
            # prefetch_related - Позволяет оптимизировать запросы к БД
            
        }
        return render(request, 'shopapp/groups-list.html', context=context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
         # Вернем пользователя на ту же страницу
        return redirect(request.path) # Если сделать просто render, только это может привести к ошибке
        # (например, пользователь сможет опубликовать такую же группу)

class ProductDetailsView(DetailView):
   template_name = 'shopapp/product-details.html'
   # model = Product
   # prefetch_related - используется для отображения связи многие ко многим
   queryset = Product.objects.prefetch_related("images")
   context_object_name = 'product'
   
   # Вернем пользователя, создателя продукта
   def get_context_data(self, **kwargs):
       context = super(ProductDetailsView, self).get_context_data()
       context['owner'] = self.object.created_by
       
       return context


class ProductsListView(ListView): # С помощью TemplateView можно делать шаблоны избегаю повторного вызова render
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False) # Изменим отображение продуктов. Выведем только те,
    # которые еще не были архивированы
    
    def get_context_data(self, **kwargs): # Метод родительского класса, который нужно переопределить для отображения продуктов
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all() # Обновляем контекст в соответствии со списком продуктов
        return context


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    def test_func(self) -> bool:
        # return self.request.user.groups.filter(name="secret-group").exists() # Пример проверки
        return self.request.user.is_superuser # Пример проверки
    model = Product
    form_class = ProductForm
    # fields = "name", "price", "description", "discount", "preview" # Указываем поля, из которых состоит модель
    success_url = reverse_lazy("shopapp:products_list") # Ленивый метод создания ссылки, только когда идет обращение к этому объекту


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'shopapp.change_product'
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    form_class = ProductForm
    template_name_suffix = "_update_form" # Необходимо сделать чтобы вместо Update не отображалось Create во View
    # Просто так не получится вернуть пользователя на страницу продуктов, поэтому надо сделать метод,
    # в котором уже можно переопределить ссылку для возврата на страницу отображения продуктов
        
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.created_by == request.user:
            return HttpResponseRedirect(reverse('shopapp:product_details', kwargs={'pk': obj.pk}))
        return super().dispatch(request, *args, **kwargs)
    # Если пользователь не является автором, он будет перенаправлен на
    # страницу с деталями продукта. Если пользователь авторизован и является автором
    # продукта, представление будет выполнено для редактирования продукта.
    
    def get_success_url(self) -> str:
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk} # На self.object в данном случае доступен тот объект,
            # обновление которого сейчас идет
        )
    # Так как было добавлено новое поле, надо определить кастомную обработку этого поля
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     for image in form.files.getlist('images'):
    #         ProductImage.objects.create(
    #             product=self.object,
    #             image=image
    #         )
    #     return response

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")
    # Напишем метод, который сделает так называемый soft-delete, то есть пометит его в списке, как архивный,
    # но не удаляет его из БД
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True # Заменим удаление на помещение в архив
        self.object.save()
        return HttpResponseRedirect(success_url)
    

class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]
    filterset_fields = ["delivery_address", "promocode", "created_at", "user", "products"]
    ordering_fields = ["user", "created_at"]
    
    
class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        # Так как на заказе есть дополнительные связи, надо сделать queryset, вместо model
        Order.objects.
        select_related("user").
        prefetch_related('products')
        
    )
    
    
class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ["shopapp.view_order",]
    queryset = (
        # Так как на заказе есть дополнительные связи, надо сделать queryset, вместо model
        Order.objects.
        select_related("user").
        prefetch_related('products')
    
    )
    
    
class OrderCreateView(CreateView):
    model = Order
    fields = "user", "products", "delivery_address", "promocode"
    success_url = reverse_lazy("shopapp:orders_list")
    
    

class OrderUpdateView(UpdateView):
    fields = "products", "user", "delivery_address", "promocode"
    template_name_suffix = "_update_form"
    queryset = (
        # Так как на заказе есть дополнительные связи, надо сделать queryset, вместо model
        Order.objects.
        select_related("user").
        prefetch_related('products')
    
    )
    
    def get_success_url(self) -> str:
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk} # На self.object в данном случае доступен тот объект,
            # обновление которого сейчас идет
        )
    
class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        elem = products_data[0]
        name = elem["name"]
        print("name:", name)
        return JsonResponse({"products": products_data})
    
    
class OrdersDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "user": order.user.username,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


class LatestProductFeed(Feed):
    title = 'Latest Products Update'
    description = 'Latest Products Updates from First Django Application'
    link = reverse_lazy("shopapp:products")
    
    def items(self):
        return (
            Product.objects
            .filter(archived=False)
            .order_by('-created_at')[:5]  # При помощи среза закгрузим только последние 5 статей
        )
    
    def item_title(self, item: Product):
        return item.name
    
    def item_description(self, item: Product):
        return item.description[:200]
