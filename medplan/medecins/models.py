from django.db import models
from users.models import CustomUser
from specialites.models import Specialite

class Medecin(models.Model):
    utilisateur = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='medecin_profile'
    )
    specialite = models.ForeignKey(
        Specialite, on_delete=models.SET_NULL, null=True, related_name='medecins'
    )
    adresse_cabinet = models.TextField()
    ville = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='medecins/', null=True, blank=True)
    est_valide = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Médecin'
        verbose_name_plural = 'Médecins'

    def __str__(self):
        return f"Dr. {self.utilisateur.last_name} {self.utilisateur.first_name}"


class Disponibilite(models.Model):
    JOURS = [
        ('lun', 'Lundi'),
        ('mar', 'Mardi'),
        ('mer', 'Mercredi'),
        ('jeu', 'Jeudi'),
        ('ven', 'Vendredi'),
        ('sam', 'Samedi'),
    ]
    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name='disponibilites'
    )
    jour = models.CharField(max_length=3, choices=JOURS)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        verbose_name = 'Disponibilité'
        verbose_name_plural = 'Disponibilités'

    def __str__(self):
        return f"{self.medecin} — {self.get_jour_display()} {self.heure_debut}→{self.heure_fin}"
