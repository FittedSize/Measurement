from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from .forms import LoginForm, UserCreationForm
from .utility import get_error_list, authenticate_user, get_confirmation_message
from uuid import uuid4
from .models import AccountAccess, User


def get_data():
    "Create initial Context data"
    return dict(
        login_page="login_page",
        home_page="home_page",
        contact_us="contact_us",
        about_us="about_us",
        logout_page="logout_page",
        user_page="user_page",
        info=False,
        success=False,
        danger=False,
        is_home=False,
        is_contact=False,
        is_about=False,
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
    data["is_contact"] = True

    return render(request, "app/contact_us.html", context=data)


def about_us(request):
    data = get_data()
    data["is_about"] = True

    return render(request, "app/about_us.html", context=data)


def logout_page(request):
    logout(request)
    return redirect(reverse("home_page"))


def verify_account(request, token):
    if request.method == "GET":
        data = get_data()
        try:
            account_access = AccountAccess.objects.get(validator_key=token)
            user = account_access.user
            user.is_active = True
            user.save()

            # the token becomes invalid after one usage
            account_access.update_validator_key()
            account_access.save()
            data["success"] = "Account Has Been Verified"
            return render(request, "app/account_verification.html", context=data)
        except AccountAccess.DoesNotExist:
            data["danger"] = "Invalid Request"
            return render(request, "app/account_verification.html", context=data)


def register_user(request):
    page_data = get_data()
    page_data["form"] = UserCreationForm()

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("user_page"))

        return render(request, "app/registration.html", context=page_data)
    elif request.method == "POST":
        data = request.POST
        form = UserCreationForm(data)
        if form.is_valid():
            form.save()
            # send verification email to user
            email = data["email"]
            user = User.objects.get(email=email)

            # Make new Account inactive until Verified through
            user.is_active = False
            user.save()

            if request.is_secure():
                base_url = f"https://{request.get_host()}/"
            else:
                base_url = f"http://{request.get_host()}/"

            base_url += "verify_account/"
            unique_key = str(uuid4()).replace("-", "")
            html_message = get_confirmation_message(unique_key, base_url)
            account_access = AccountAccess.objects.create(
                validator_key=unique_key, user=user
            )
            account_access.save()

            send_mail(
                "Account Confirmation",
                "Click the link to verify your account",
                from_email=None,
                recipient_list=[email],
                html_message=html_message,
            )

            page_data[
                "success"
            ] = "Registration SucessFull Check your Email for Verification"

            return render(request, "app/registration.html", context=page_data)
        page_data["danger"] = get_error_list(form.errors)
        return render(request, "app/registration.html", context=page_data)
