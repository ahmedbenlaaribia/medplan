from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'users/login.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect.'})


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'users/register.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'users/register.html', {
                'error': 'Les mots de passe ne correspondent pas.',
                'data': request.POST
            })
            
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {
                'error': 'Ce nom d\'utilisateur existe déjà.',
                'data': request.POST
            })

        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            telephone=telephone,
            role='patient'
        )
        
        login(request, user)
        return redirect('home')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
