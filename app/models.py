from django.db import models
from .utility import validate_positive
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    INDIVIDUAL = "IN"
    BUSINESS = "BU"
    ACCOUNTS = [(INDIVIDUAL, "Individual"), (BUSINESS, "Business")]
    account_type = models.CharField(choices=ACCOUNTS, max_length=2, default=INDIVIDUAL)


class Trouser(models.Model):
    length = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="Trouser length taken in standing position",
        validators=[validate_positive],
    )
    waist = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="waist measurement taken around the waist",
        validators=[validate_positive],
    )
    thigh = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="thigh measurement taken around the thigh",
        validators=[validate_positive],
    )
    calf = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="calf measurement taken around the calf",
        validators=[validate_positive],
    )
    ankle = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="ankle measurement taken around the ankle",
        validators=[validate_positive],
    )

    def __str__(self):
        return f"Trouser length: {self.length}"
