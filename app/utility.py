from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model

import json


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
