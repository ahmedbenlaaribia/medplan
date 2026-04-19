from django.db import models
from users.models import CustomUser
from medecins.models import Medecin

class RendezVous(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='mes_rendez_vous'
    )
    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name='rendez_vous'
    )
    date = models.DateField()
    heure = models.TimeField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    motif = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'
        ordering = ['date', 'heure']

    def __str__(self):
        return f"{self.patient} → {self.medecin} le {self.date} à {self.heure}"
