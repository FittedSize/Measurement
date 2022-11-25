from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from uuid import uuid4

import json


def generate_key():
    return str(uuid4).replace("-", "")


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
