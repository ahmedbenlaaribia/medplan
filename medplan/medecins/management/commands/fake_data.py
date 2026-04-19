from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.models import CustomUser
from specialites.models import Specialite
from medecins.models import Medecin, Disponibilite
from rendez_vous.models import RendezVous

class Command(BaseCommand):
    help = 'Genere des donnees fictives'

    def handle(self, *args, **options):
        faker = Faker('fr_FR')

        # Creer les specialites
        noms_specialites = [
            'Cardiologie', 'Dermatologie', 'Pediatrie',
            'Neurologie', 'Ophtalmologie', 'Dentiste'
        ]
        specialites = []
        for nom in noms_specialites:
            slug = nom.lower().replace(' ', '-')
            s, created = Specialite.objects.get_or_create(nom=nom, slug=slug)
            specialites.append(s)
            self.stdout.write(f'Specialite: {nom}')

        # Creer des medecins
        villes = ['Casablanca', 'Rabat', 'Marrakech', 'Fes', 'Agadir']
        jours = ['lun', 'mar', 'mer', 'jeu', 'ven']

        for i in range(10):
            user = CustomUser.objects.create_user(
                username=faker.user_name() + str(i),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                password='password123',
                role='medecin',
            )
            medecin = Medecin.objects.create(
                utilisateur=user,
                specialite=random.choice(specialites),
                ville=random.choice(villes),
                adresse_cabinet=faker.address(),
                tarif=random.randint(100, 500),
                description=faker.text(max_nb_chars=200),
                est_valide=True,
            )
            for jour in random.sample(jours, 3):
                Disponibilite.objects.create(
                    medecin=medecin,
                    jour=jour,
                    heure_debut='09:00',
                    heure_fin='17:00',
                )
            self.stdout.write(f'Medecin {i+1} cree: {medecin}')

        # Creer des patients
        patients = []
        for i in range(5):
            user = CustomUser.objects.create_user(
                username=faker.user_name() + 'p' + str(i),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                password='password123',
                role='patient',
            )
            patients.append(user)
            self.stdout.write(f'Patient {i+1} cree: {user}')

        # Creer des rendez-vous
        medecins = list(Medecin.objects.all())
        statuts = ['en_attente', 'confirme', 'annule', 'termine']
        for i in range(20):
            RendezVous.objects.create(
                patient=random.choice(patients),
                medecin=random.choice(medecins),
                date=faker.date_between(start_date='-30d', end_date='+30d'),
                heure=f'{random.randint(8, 16):02d}:00',
                statut=random.choice(statuts),
                motif=faker.sentence(),
            )
        self.stdout.write(f'20 rendez-vous crees')
        self.stdout.write(self.style.SUCCESS('Fake data generated successfully!'))