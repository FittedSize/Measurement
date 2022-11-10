from django.contrib import admin
from .models import Trouser, User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.register(Trouser)
class TrouserAdmin(admin.ModelAdmin):
    pass
