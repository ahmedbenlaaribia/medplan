from django.contrib import admin
from .models import RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date', 'heure', 'statut')
    list_filter = ('statut', 'date')
    search_fields = ('patient__last_name', 'medecin__utilisateur__last_name')
