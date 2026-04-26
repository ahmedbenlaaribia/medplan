# Authentication Implementation Summary

This document outlines the additions and modifications made to the `MediRDV` project to implement the user authentication system.

## 1. URL Configurations
- **`medplan/users/urls.py`**: Created a new file to route the authentication views:
  - `/users/login/` -> `LoginView`
  - `/users/register/` -> `RegisterView`
  - `/users/logout/` -> `LogoutView`
- **`medplan/medplan/urls.py`**: Updated the global URL configuration to include the new `users.urls` at the `/users/` path.

## 2. Views
- **`medplan/users/views.py`**: Created class-based views strictly using `django.views.View`:
  - `LoginView`: Handles `GET` (shows form) and `POST` (authenticates and logs in the user, or returns an error message).
  - `RegisterView`: Handles `GET` (shows form) and `POST` (validates input, checks for matching passwords and existing usernames, creates a new `CustomUser` with the role `patient`, logs the user in, and redirects to the home page).
  - `LogoutView`: Logs the user out and redirects to the login page.

## 3. Templates
- **`templates/users/login.html`**: Created the login page extending `base/base.html` and using existing plain CSS classes like `.card`, `.field`, and `.btn`. Includes CSRF token and error message display.
- **`templates/users/register.html`**: Created the registration page extending `base/base.html` and using plain CSS. It includes fields for first name, last name, username, email, telephone, password, and password confirmation.
- **`templates/base/base.html`**: Updated the desktop navigation bar and mobile drawer to dynamically display links:
  - For unauthenticated users: Shows "Connexion" and "S'inscrire".
  - For authenticated users: Shows the user's name (or username) and a "Déconnexion" (Logout) link.

## 4. Protected Views
- **`medplan/rendez_vous/views.py`**: Protected both `RendezVousListView` and `RendezVousCreateView` by adding a manual authentication check (`if not request.user.is_authenticated: return redirect('login')`) at the beginning of their respective `get()` and `post()` methods. This ensures only logged-in users can view or create appointments.

## 5. Constraints Followed
- Used only class-based views inheriting from `django.views.View`.
- Used only `get()` and `post()` methods.
- No external CSS frameworks like Bootstrap were used.
- Existing models, `manage.py`, and `settings.py` were left untouched.
- `{% csrf_token %}` and `{% extends 'base/base.html' %}` were strictly implemented in the new forms.
