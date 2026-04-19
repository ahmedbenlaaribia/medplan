from django.contrib import admin
from .models import Specialite

@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}
