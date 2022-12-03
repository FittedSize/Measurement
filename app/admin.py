from django.contrib import admin
from .models import Trouser, User, Record, Measurement, Shirt, AccountAccess
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["first_name", "last_name", "account_type"]


@admin.register(Trouser)
class TrouserAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ["user"]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    pass


@admin.register(Shirt)
class ShirtAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountAccess)
class AccountAccessAdmin(admin.ModelAdmin):
    pass
