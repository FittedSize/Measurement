from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import LoginForm
from .utility import get_error_list, authenticate_user


def get_data():
    "Create initial Context data"
    return dict(
        login_page="login_page",
        home_page="home_page",
        contact_us="contact_us",
        about_us="about_us",
        logout_page="logout_page",
        info=False,
        success=False,
        danger=False,
        is_home=False,
    )


@login_required(login_url="/login_page")
def user_page(request):
    data = get_data()
    return render(request, "app/user_page.html", context=data)


def home_page(request):
    data = get_data()
    data["is_home"] = True
    return render(request, "app/index.html", context=data)


def login_page(request):
    data = get_data()
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("home_page"))
        return render(request, "app/login.html", context=data)
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate_user(
                email=request.POST["email"],
                password=request.POST["password"],
            )
            if user:
                login(request, user)
                return redirect(reverse("user_page"))
            data["danger"] = ["Invalid Email or Password"]
            return render(request, "app/login.html", context=data)

        data["danger"] = get_error_list(form.errors)
        return render(request, "app/login.html", context=data)


def contact_us(request):
    data = get_data()
    return render(request, "app/contact_us.html", context=data)


def about_us(request):
    data = get_data()
    return render(request, "app/about_us.html", context=data)


def logout_page(request):
    logout(request)
    return redirect(reverse("home_page"))
