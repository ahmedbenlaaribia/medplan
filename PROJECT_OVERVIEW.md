# MediRDV - Architecture & Project Overview

This document serves as a comprehensive guide to the **MediRDV** Django project. It describes the architecture, functionalities, business logic, and database schema. This file is designed to give any AI or developer a complete, detailed understanding of the project without needing to read the source code.

---

## 1. Project Overview & Architecture

**MediRDV** is a web-based medical appointment management platform built with Django. It connects patients with doctors, allowing patients to search for specialists, view their profiles, and book appointments. 

### Architecture Style
- **Monolithic Django Application**: The project uses Django's standard MTV (Model-Template-View) architecture.
- **Class-Based Views (Strict)**: The project strictly uses basic `View` classes (`from django.views import View`) rather than Django's generic views (`ListView`, `DetailView`, etc.). All logic is handled explicitly inside `get()` and `post()` methods.
- **Frontend Stack**: Vanilla HTML and CSS. **No external frameworks (like Bootstrap or Tailwind) are used.** All styling is done via plain CSS in a single `style.css` file. Interactions like live search are built using Vanilla JavaScript (ES6+ Fetch API).
- **Template Inheritance**: Every HTML template extends a global `base/base.html` template.

---

## 2. Database Schema & Models

The database handles relational mapping between users, roles, medical data, and schedules. It uses **PostgreSQL**.

### App: `users`
- **`CustomUser`** *(extends `AbstractUser`)*
  - `role`: CharField with choices `patient` or `medecin`.
  - `telephone`: CharField.
  - `adresse`: TextField.
  - *Logic*: Replaces the default Django user model.

### App: `specialites`
- **`Specialite`**
  - `nom`: CharField (e.g., Cardiologie, Dermatologie).
  - `slug`: SlugField.

### App: `medecins`
- **`Medecin`**
  - `utilisateur`: OneToOneField linked to `CustomUser`.
  - `specialite`: ForeignKey linked to `Specialite`.
  - `ville`: CharField.
  - `adresse_cabinet`: TextField.
  - `tarif`: IntegerField (consultation price in MAD).
  - `description`: TextField.
  - `photo`: ImageField.
  - `est_valide`: BooleanField (controls visibility on the platform).
- **`Disponibilite`**
  - `medecin`: ForeignKey linked to `Medecin` (related_name usually `disponibilites` or default).
  - `jour`: CharField with choices (lun, mar, mer, jeu, ven, sam).
  - `heure_debut`: TimeField.
  - `heure_fin`: TimeField.

### App: `rendez_vous`
- **`RendezVous`**
  - `patient`: ForeignKey linked to `CustomUser`.
  - `medecin`: ForeignKey linked to `Medecin`.
  - `date`: DateField.
  - `heure`: TimeField.
  - `statut`: CharField with choices (`en_attente`, `confirme`, `annule`, `termine`).
  - `motif`: TextField.
  - `created_at`: DateTimeField (auto_now_add=True).

---

## 3. Functionalities & App Logic

### A. Authentication & User Management (`users`)
- **Routes**: `/users/login/`, `/users/register/`, `/users/logout/`
- **Logic**: 
  - Uses `authenticate()`, `login()`, and `logout()`.
  - Views are class-based. 
  - Unauthenticated users see login/register links in the navbar; authenticated users see their name and logout.
  - *Doctor Restrictions*: Doctors currently have their passwords disabled (set to unusable) in the mock data, making the site "patient-centric" for now. The doctor dashboard was temporarily removed.

### B. Doctor Directory & Search (`medecins`)
- **Routes**: `/medecins/` (List), `/medecins/<id>/` (Detail)
- **Search Logic (`MedecinListView`)**: 
  - Filters by `est_valide=True`.
  - Accepts `nom`, `ville`, and `specialite` as GET parameters.
  - `nom` searches across **both** `CustomUser.first_name` and `CustomUser.last_name` using Django's `Q` objects (`Q(utilisateur__first_name__icontains=nom) | Q(utilisateur__last_name__icontains=nom)`).
- **Live Search (Frontend)**:
  - The list page implements a Vanilla JS live search.
  - It listens to `input` and `change` events on the search form, uses `fetch()` to request the updated URL, parses the returned HTML string using `DOMParser`, and hot-swaps the `.ml-grid` and `.ml-meta` components in the DOM without a full page reload.

### C. Appointment Booking (`rendez_vous`)
- **Routes**: `/rendez-vous/`
- **Logic**: 
  - Protected views: Logic explicitly checks `if not request.user.is_authenticated: return redirect('login')`.
  - Allows patients to create an appointment (`RendezVous`) with a specific doctor for a specific date and time.
  - Lists the patient's upcoming and past appointments.

### D. Mock Data Generation (Management Commands)
- **`setup_doctors.py`** *(located in `medecins/management/commands/`)*
  - Automates database seeding.
  - **Clearing mechanism**: Deletes data in strict reverse-relational order to prevent foreign key constraint errors (`RendezVous` -> `Disponibilite` -> `Medecin` -> `Specialite` -> `CustomUser(role=medecin)`).
  - **Seeding mechanism**: Generates 7 medical specialties and exactly 3 doctors per specialty (21 total).
  - **Security**: newly generated doctors are created with `user.set_unusable_password()` to prevent unauthorized logins while the doctor portal is inactive.

---

## 4. Strict Project Rules & Conventions

If an LLM or developer is modifying this project, they **MUST** adhere to the following rules:

1. **Class-Based Views Only**: Use `django.views.View`. Never use function-based views or Django Generic Views (`ListView`, `UpdateView`, etc.).
2. **Explicit HTTP Methods**: Inside the class-based views, strictly define `def get(self, request):` and `def post(self, request):`. Use `render()` or `redirect()` to return HTTP responses.
3. **No CSS Frameworks**: All styling must be written in pure CSS inside `static/base/css/style.css`. Classes like Bootstrap or Tailwind are strictly forbidden.
4. **No External Packages**: Do not run `pip install`. The project must rely purely on standard Django.
5. **Template Extension**: Every new template must start with `{% extends 'base/base.html' %}`.
6. **Form Security**: Every HTML `<form>` must include `{% csrf_token %}`.
7. **Manual View Protection**: Do not use `@login_required` decorators. Instead, at the top of protected `get`/`post` methods, explicitly write:
   ```python
   if not request.user.is_authenticated:
       return redirect('login')
   ```
8. **No Model/Settings Modification**: Existing models, `settings.py`, and `manage.py` should generally not be modified unless explicitly instructed.
