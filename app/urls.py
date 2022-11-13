from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home_page"),
    path("login/", views.login, name="login_page"),
]
