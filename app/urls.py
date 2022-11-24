from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("login_page/", views.login_page, name="login_page"),
    path("logout_page/", views.logout_page, name="logout_page"),
    path("about/", views.about_us, name="about_us"),
    path("contact/", views.contact_us, name="contact_us"),
    path("user_page/", views.user_page, name="user_page"),
    path("register_user/", views.register_user, name="register_user"),
]
