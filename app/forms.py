from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gtl
from django.contrib.auth import hashers

from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
            "account_type",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
            raise ValidationError(gtl("Account with this email already exist"))
        except User.DoesNotExist:
            return email

    def clean(self):
        clean_data = super().clean()
        passwd1 = clean_data.get("password")
        passwd2 = clean_data.get("confirm_password")
        if passwd1 != passwd2:
            msg = "Password Mismatch"

            self.add_error("password", msg)
            self.add_error("confirm_password", msg)
        else:
            # hash the password
            password = hashers.make_password(self.cleaned_data["password"])
            self.cleaned_data["password"] = password
