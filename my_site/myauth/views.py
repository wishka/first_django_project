from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from .models import Profile
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


@user_passes_test(lambda u: u.is_superuser) # Может отправить в бесконечный цикл
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default_value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spamm-eggs'
    return HttpResponse("Session set")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default_value')
    return HttpResponse(f"Session value: {value!r}")