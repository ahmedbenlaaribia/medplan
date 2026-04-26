from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import RendezVous
from medecins.models import Medecin

class RendezVousListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        rdvs = RendezVous.objects.filter(patient=request.user)
        return render(request, 'rendez_vous/list.html', {'rdvs': rdvs})

class RendezVousCreateView(View):
    def get(self, request, medecin_id):
        if not request.user.is_authenticated:
            return redirect('login')
        medecin = get_object_or_404(Medecin, pk=medecin_id)
        return render(request, 'rendez_vous/create.html', {'medecin': medecin})

    def post(self, request, medecin_id):
        if not request.user.is_authenticated:
            return redirect('login')
        medecin = get_object_or_404(Medecin, pk=medecin_id)
        RendezVous.objects.create(
            patient=request.user,
            medecin=medecin,
            date=request.POST.get('date'),
            heure=request.POST.get('heure'),
            motif=request.POST.get('motif', ''),
        )
        return redirect('rdv_list')