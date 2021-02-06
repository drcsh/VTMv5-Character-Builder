from django.contrib import admin
from .models import Chronicle

# Register your models here.

@admin.register(Chronicle)
class ChronicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'storyteller')
