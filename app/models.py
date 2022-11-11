from django.db import models
from .utility import validate_positive
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    INDIVIDUAL = "IN"
    BUSINESS = "BU"
    ACCOUNTS = [(INDIVIDUAL, "Individual"), (BUSINESS, "Business")]
    account_type = models.CharField(choices=ACCOUNTS, max_length=2, default=INDIVIDUAL)

    REQUIRED_FIELDS = ["first_name", "last_name", "account_type"]

    @property
    def is_business(self):
        return self.account_type == self.BUSINESS

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_business:
            user_record = Record.objects.filter(owner=self)
            if user_record.count() == 1:
                user_record = user_record[0]
            else:
                user_record = None

            user_record = user_record or Record.objects.create(owner=self)
            user_record.save()


class Shirt(models.Model):
    length = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="Measured from the top of collar-bone to any desired length",
        validators=[validate_positive],
    )
    burst = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="Taken around the widest portion of the chest",
        validators=[validate_positive],
    )
    hip = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="Taken around the widest portion of the hip",
        validators=[validate_positive],
    )
    shoulder = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="Taken accross the shoulder",
        validators=[validate_positive],
    )
    neck = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="Taken loosely around the neck",
        validators=[validate_positive],
    )
    sleeve = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        help_text="Taken from the nape of neck to the wrist",
        validators=[validate_positive],
    )
    fitted = models.BooleanField(default=True, help_text="Do you want a fitted shirt")


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
    fitted = models.BooleanField(default=True, help_text="Do you want a fitted trouser")

    def __str__(self):
        return f"Trouser length: {self.length}"


class Profile(models.Model):
    username = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)

    def __str__(self):
        return f"Profile of {self.username.title()}"


class Measurement(models.Model):
    trouser = models.ForeignKey(Trouser, on_delete=models.CASCADE)
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Record(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    customers = models.ManyToManyField(Profile, blank=True)

    def __str__(self):
        return f"Record of {self.owner.username.title()}"
