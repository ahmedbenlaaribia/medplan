from django.contrib import admin
from .models import Medecin, Disponibilite

@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'specialite', 'ville', 'tarif', 'est_valide')
    list_filter = ('specialite', 'est_valide', 'ville')
    search_fields = ('utilisateur__last_name', 'ville')

@admin.register(Disponibilite)
class DisponibiliteAdmin(admin.ModelAdmin):
    list_display = ('medecin', 'jour', 'heure_debut', 'heure_fin')
    list_filter = ('jour',)