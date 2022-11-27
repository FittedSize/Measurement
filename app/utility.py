from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from uuid import uuid4
import re
from string import ascii_lowercase, ascii_uppercase, punctuation, digits

import json


def generate_key():
    return str(uuid4()).replace("-", "")


def validate_positive(value):
    if value < 0:
        raise ValidationError(
            gettext_lazy("%(value)s is not a positive number"),
            params={"value": value},
        )


def get_error_list(form_errors):
    "Convert given form_errors to List of errors"
    error_list = []
    for _, value in json.loads(form_errors.as_json()).items():
        error_list.append(value[0]["message"])
    return list(set(error_list))


def authenticate_user(email, password):
    "Custom Authentication method using email and password"
    try:
        user = get_user_model().objects.get(email=email)
        if user.check_password(password):
            return user
        else:
            return None
    except get_user_model().DoesNotExist:
        return None


def get_confirmation_message(unique_key, base_url="http://127.0.0.1:8000/"):
    template = """
        <!doctype html>
        <html lang="en">
          <head>
          <style>
          .logo{{
            display:block;
            width: 60px;
            height: 60px;
            border-radius: 50%;
          }}
          .content{{
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
          }}
        </style>
        </head>
        <body>
        <div class="content">
          <img class="logo"
          src="https://measure-it.s3.amazonaws.com/images/smart_measure_logo.png"/>
        </div></br>
          <p> Click on the link below to activate your account </p></br>
        <a href="{base_url}{unique_key}"><h4>{base_url}{unique_key}</h4></a>
        </body>
      </html>
  """
    return template.format(base_url=base_url, unique_key=unique_key)


def get_password_reset_message(unique_key, base_url="http://127.0.0.1:8000/"):
    template = """
        <!doctype html>
        <html lang="en">
          <head>
          <style>
          .logo{{
            display:block;
            width: 60px;
            height: 60px;
            border-radius: 50%;
          }}
          .content{{
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
          }}
        </style>
        </head>
        <body>
        <div class="content">
          <img class="logo"
          src="https://measure-it.s3.amazonaws.com/images/smart_measure_logo.png"/>
        </div></br>
          <p> Click the link below to reset your account Password</p></br>
          <p> Please Ignore if you did not make the request</p></br>
        <a href="{base_url}{unique_key}"><h4>{base_url}{unique_key}</h4></a>
        </body>
      </html>
    """
    return template.format(base_url=base_url, unique_key=unique_key)


def validate_password(value):
    if len(value) < 8:
        raise ValidationError(gettext_lazy("minimum password length is 8"))
    elif not re.findall(f"[{digits}]", value):
        raise ValidationError(gettext_lazy("Password must contain at least 1 digit"))
    elif not re.findall(f"[{ascii_lowercase}]", value):
        raise ValidationError(gettext_lazy("Password must include lowercase"))
    elif not re.findall(f"[{ascii_uppercase}]", value):
        raise ValidationError(gettext_lazy("Password must include uppercase"))
    elif not re.findall(f"[{punctuation}]", value):
        raise ValidationError(gettext_lazy("Password must include at least 1 symbol"))
