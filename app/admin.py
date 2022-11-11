from django.contrib import admin
from .models import Trouser, User, Record, Profile, Measurement, Shirt
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["first_name", "last_name", "account_type"]


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass


@admin.register(Trouser)
class TrouserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    pass


@admin.register(Shirt)
class ShirtAdmin(admin.ModelAdmin):
    pass
