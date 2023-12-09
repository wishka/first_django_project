from timeit import default_timer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import GroupForm
from .models import Product, Order
from .permissions import IsProductAuthor

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'shopapp/shop-index.html')
    

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
   model = Product
   context_object_name = 'product'
   # context = {
   #     "created_by": Product.created_by
   # }


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
    fields = "name", "price", "description", "discount" # Указываем поля, из которых состоит модель
    success_url = reverse_lazy("shopapp:products_list") # Ленивый метод создания ссылки, только когда идет обращение к этому объекту
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form" # Необходимо сделать чтобы вместо Update не отображалось Create во View
    # Просто так не получится вернуть пользователя на страницу продуктов, поэтому надо сделать метод,
    # в котором уже можно переопределить ссылку для возврата на страницу отображения продуктов
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.object.author == self.request.user
        
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
    fields = "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    fields = "products", "user"
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
