from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (get_cookie_view, set_cookie_view, AboutMeView,
                    RegisterView, UserListView, UserDetailView, UserUpdateAvatarView,
                    set_session_view, get_session_view, MyLogoutView,
                    FooBarView, update_profile, HelloView)


app_name = "myauth"
# Обращение к ссылками на страницах всегда идет по имени - name
urlpatterns = [
    # path("login/", login_view, name="login"),
    # LoginView ищет стандартную страницу аутентификации(registration.html) чтобы это изменить
    # добавим свою страницу
    path("login/", LoginView.as_view(
        template_name="myauth/login.html",
        redirect_authenticated_user=True
    ), name="login"),
    # path("logout/", logout_view, name="logout"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("hello/", HelloView.as_view(), name="hello"),
    path("register/", RegisterView.as_view(), name="register"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path('about-me/update/', update_profile, name='profile_update'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/update-avatar/', UserUpdateAvatarView.as_view(), name='user_update_avatar'),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("session/get/", get_session_view, name="session-get"),
    path("session/set/", set_session_view, name="session-set"),
    
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]