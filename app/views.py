from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import hashers
from .forms import LoginForm, UserCreationForm, PasswordResetForm
from .utility import (
    get_error_list,
    authenticate_user,
    get_confirmation_message,
    get_password_reset_message,
)
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


def forgot_password(request):
    context = get_data()
    if request.method == "GET":
        return render(request, "app/forgot_password.html", context=context)
    elif request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            account_access = AccountAccess.objects.get(user=user)
            if request.is_secure():
                base_url = f"https://{request.get_host()}/"
            else:
                base_url = f"http://{request.get_host()}/"

            base_url += "account/forgot_password/"
            unique_key = account_access.password_reset_key
            html_message = get_password_reset_message(unique_key, base_url)

            send_mail(
                "Password Reset",
                "Click the link below to reset your Password",
                from_email=None,
                recipient_list=[email],
                html_message=html_message,
            )

            context["success"] = "Reset Link Sent to Your email"
            return render(request, "app/forgot_password.html", context=context)

        except User.DoesNotExist:
            context["danger"] = [f"No User with {email}"]
            return render(request, "app/forgot_password.html", context=context)


def reset_password(request, token):
    context = get_data()
    if request.method == "GET":
        try:
            account_access = AccountAccess.objects.get(password_reset_key=token)
            return render(request, "app/reset_password.html")
        except AccountAccess.DoesNotExist:
            context["danger"] = ["Invalid Request"]
            return render(request, "app/invalid_request.html", context=context)

    elif request.method == "POST":
        try:
            account_access = AccountAccess.objects.get(password_reset_key=token)
            user = account_access.user
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                password = hashers.make_password(form.data.get("password1"))
                user.password = password
                user.save()
                context["success"] = ["Password Reset Successfull"]
                return render(request, "app/reset_password_status.html", context=context)
            else:
                context["danger"] = get_error_list(form.errors)
                return render(request, "app/reset_password.html", context=context)
        except AccountAccess.DoesNotExist:
            context["danger"] = ["Invalid Request"]
            return render(request, "app/invalid_request.html", context=context)
