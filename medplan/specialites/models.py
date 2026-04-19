from django.db import models

class Specialite(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Spécialité'
        verbose_name_plural = 'Spécialités'

    def __str__(self):
        return self.nom
