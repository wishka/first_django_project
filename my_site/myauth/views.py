from random import random
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.utils.decorators import method_decorator
# from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _, ngettext
# Теперь к функции gettext можно обращаться через _. Позволяет переводить объекты на
# верхнем уровне, то есть там, где еще не известна локализация пользователя
# Ленивый перевод это подготовка к переводу
# ngettext - используется для плюрализации(изменению окончаний названий в соответствии с количеством)
# 1 товар, 10 товаров и тд

from .forms import ProfileForm
from .models import Profile


# Ленивые функции позволяют возвращать объекты не в момент вызова функции, а в
# момент обращения к полученному объекту
# Для создания переводов выполним в терминале python manage.py makemessages -l ru
# А после этого для компиляции всех переведенных слов
class HelloView(View):
    welcome_message = _("Hello world")
    def get(self, request: HttpRequest) -> HttpResponse:
        items_string = request.GET.get('items') or 0
        items = int(items_string)
        products_line = ngettext(
            'one product',
            '{count} products',
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(f"<h1>{self.welcome_message}</h1>"
                            f"\n<h2>{products_line}</h2>")
        
class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"
    

class RegisterView(CreateView):
    form_class = UserCreationForm# Необходимо указывать форму, на основе которой будет создана новая сущность
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")
    
    # Чтобы произвести аутентификацию пользователя, надо доработать класс
    # переопределив метод
    def form_valid(self, form):
        response = super().form_valid(form)
        # Лучше связать создание профиля при создании нового пользователя
        Profile.objects.create(user=self.object) # self.object - сохраняется сразу по form_valid()
        # Данные о пользователе и пароле надо вытащить из формы
        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password)
        login(self.request, user=user)
        # Profile.objects.create(user=user) # Так не желательно,
        # потому что так мы завязываем эту логику с аутентификацией пользователя
        return response
    
    
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/shopapp/products-list')
        return render(request, '/shopapp/products-list')
    
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/shopapp/products-list')
    return render(request, "myauth/login.html", {'Error': 'Invalid credentials'})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


@cache_page(60 * 2) # Добавим кеширование странцы на 2 мин
@user_passes_test(lambda u: u.is_superuser) # Может отправить в бесконечный цикл
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default_value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spamm-eggs'
    return HttpResponse("Session set")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default_value')
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
    

def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'myauth/about-me.html')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'myauth/profile_update.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = Profile
    template_name = 'myauth/user-list.html'
    context_object_name = 'profiles'
    
    def user_list_view(request):
        users = User.objects.all()
        return render(request, 'user-list.html', {'users': users})
    
    def get_queryset(self):
        return super().get_queryset()


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = Profile
    # queryset = User.objects.prefetch_related("profile")
    template_name = 'myauth/user_detail.html'
    context_object_name = 'user'
    
    def get_queryset(self):
        # Вы вызываете prefetch_related, чтобы сократить количество запросов к базе данных
        return User.objects.prefetch_related("profile")
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = context['user']  # 'user' вместо 'profile', чтобы избежать путаницы
        context['can_update_avatar'] = self.request.user.is_staff or self.request.user == user
        return context


# @method_decorator(staff_member_required, name='dispatch')
class UserUpdateAvatarView(UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'myauth/user_update_avatar.html'
    fields = ['avatar']
    context_object_name = 'profile'
    
    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        return self.request.user == profile.user or self.request.user.is_staff
    
    def get_success_url(self):
        # возвращает пользователя на страницу его профиля после изменения аватара
        return reverse('profile_detail', kwargs={'pk': self.request.user.profile.pk})
    
    def get_queryset(self):
        # Здесь можно добавить более специфичную логику, если необходимо
        return Profile.objects.select_related('user').filter(user=self.request.user)
