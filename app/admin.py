from django.contrib import admin
from .models import Trouser


@admin.register(Trouser)
class TrouserAdmin(admin.ModelAdmin):
    pass
