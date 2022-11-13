from django.shortcuts import render

data = dict(login_page="login_page", home_page="home_page")


def home(request):
    return render(request, "app/index.html", context=data)


def login(request):
    return render(request, "app/login.html", context=data)
