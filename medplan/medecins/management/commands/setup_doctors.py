import random
from django.core.management.base import BaseCommand
from users.models import CustomUser
from specialites.models import Specialite
from medecins.models import Medecin, Disponibilite
from rendez_vous.models import RendezVous

class Command(BaseCommand):
    help = 'Setup specific doctors and specialities'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        RendezVous.objects.all().delete()
        Disponibilite.objects.all().delete()
        Medecin.objects.all().delete()
        Specialite.objects.all().delete()
        CustomUser.objects.filter(role='medecin').delete()

        specialites_data = [
            ('Cardiologie', 'cardiologie'),
            ('Dermatologie', 'dermatologie'),
            ('Dentiste', 'dentiste'),
            ('Pediatrie', 'pediatrie'),
            ('Neurologie', 'neurologie'),
            ('Ophtalmologie', 'ophtalmologie'),
            ('Endocrinologie', 'endocrinologie')
        ]
        
        specialites_objs = []
        for nom, slug in specialites_data:
            specialites_objs.append(Specialite.objects.create(nom=nom, slug=slug))

        villes = ['Casablanca', 'Rabat', 'Marrakech', 'Fes', 'Agadir', 'Tanger']
        prenoms = ['Hassan', 'Youssef', 'Mehdi', 'Amine', 'Fatima', 'Khadija', 'Salma', 'Meryem', 'Omar', 'Karim', 'Sanaa', 'Nadia', 'Tariq', 'Rachid', 'Ali', 'Sara', 'Zineb', 'Hicham', 'Yassine', 'Adil', 'Mounir']
        noms = ['Alaoui', 'Bennani', 'Tazi', 'El Fassi', 'Benjelloun', 'Berrada', 'Chraibi', 'Guessous', 'Idrissi', 'Ouazzani', 'Kabbaj', 'Benkirane', 'Lahlou', 'Filali', 'Zemmouri']

        created_doctors = []
        jours = ['lun', 'mar', 'mer', 'jeu', 'ven', 'sam']
        
        self.stdout.write("Creating new data...")
        for spec in specialites_objs:
            for _ in range(3):
                first_name = random.choice(prenoms)
                last_name = random.choice(noms)
                username = f"{first_name.lower()}.{last_name.lower()}"
                
                # ensure username is unique
                while CustomUser.objects.filter(username=username).exists():
                    username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 100)}"

                user = CustomUser.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    role='medecin'
                )
                user.set_unusable_password()
                user.save()

                ville = random.choice(villes)
                medecin = Medecin.objects.create(
                    utilisateur=user,
                    specialite=spec,
                    ville=ville,
                    adresse_cabinet=f"Centre Medical, {ville}",
                    tarif=random.randint(15, 50) * 10,
                    description=f"Médecin spécialiste en {spec.nom}.",
                    est_valide=True
                )

                selected_jours = random.sample(jours, 3)
                for jour in selected_jours:
                    Disponibilite.objects.create(
                        medecin=medecin,
                        jour=jour,
                        heure_debut='09:00',
                        heure_fin='17:00'
                    )

                created_doctors.append({
                    'name': f"{first_name} {last_name}",
                    'username': username,
                    'password': 'Désactivé',
                    'specialite': spec.nom,
                    'ville': ville
                })

        self.stdout.write("\n=== Summary of Created Doctors ===")
        self.stdout.write(f"{'Full Name':<25} | {'Username':<20} | {'Password':<15} | {'Specialite':<20} | {'Ville'}")
        self.stdout.write("-" * 100)
        for doc in created_doctors:
            self.stdout.write(f"{doc['name']:<25} | {doc['username']:<20} | {doc['password']:<15} | {doc['specialite']:<20} | {doc['ville']}")
        self.stdout.write("-" * 100)
        self.stdout.write(self.style.SUCCESS('Successfully created specific data'))
