from django.db import models
from .utility import validate_positive, generate_key
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class BusinessAccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(account_type="BU")


class IndividualAccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(account_type="IN")


class User(AbstractUser):
    INDIVIDUAL = "IN"
    BUSINESS = "BU"
    ACCOUNTS = [(INDIVIDUAL, "Individual"), (BUSINESS, "Business")]
    account_type = models.CharField(choices=ACCOUNTS, max_length=2, default=INDIVIDUAL)
    REQUIRED_FIELDS = ["first_name", "last_name", "account_type", "email"]

    @property
    def is_business(self):
        return self.account_type == self.BUSINESS

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_business:
            user_record = Record.objects.filter(user=self)
            if user_record.count() == 1:
                user_record = user_record[0]
            else:
                user_record = None

            user_record = user_record or Record.objects.create(user=self)
            user_record.save()

        # create an AccountAccess for user if it does not exist
        try:
            account_access = AccountAccess.objects.get(user=self)
        except AccountAccess.DoesNotExist:
            account_access = AccountAccess(user=self)
            account_access.save()

    # objects = models.Manager()
    # business = BusinessAccountManager()
    # personal = IndividualAccountManager()


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

    def __str__(self):
        return f"Shirt {self.id}"


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
        return f"Trouser: {self.id}"


class Record(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username.title()} Record"


class Measurement(models.Model):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=False)
    trouser = models.OneToOneField(
        Trouser, on_delete=models.SET_NULL, null=True, blank=True
    )
    shirt = models.OneToOneField(Shirt, on_delete=models.SET_NULL, null=True, blank=True)
    record = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Measurement: {self.email}"


class AccountAccess(models.Model):
    validator_key = models.SlugField(default=generate_key())
    password_reset_key = models.SlugField(default=generate_key())
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account_access"
    )

    def update_password_reset_key(self):
        self.password_retrieve_key = generate_key()

    def update_validator_key(self):
        self.validator_key = generate_key()

    def __str__(self):
        return f"{self.user.username.title()} key"
