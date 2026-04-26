from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Q
from .models import Medecin
from specialites.models import Specialite

class MedecinListView(View):
    def get(self, request):
        medecins = Medecin.objects.filter(est_valide=True)
        specialites = Specialite.objects.all()
        specialite_id = request.GET.get('specialite')
        ville = request.GET.get('ville')
        nom = request.GET.get('nom')
        if specialite_id:
            medecins = medecins.filter(specialite__id=specialite_id)
        if ville:
            medecins = medecins.filter(ville__icontains=ville)
        if nom:
            medecins = medecins.filter(Q(utilisateur__first_name__icontains=nom) | Q(utilisateur__last_name__icontains=nom))
        context = {'medecins': medecins, 'specialites': specialites}
        return render(request, 'medecins/list.html', context)

class MedecinDetailView(View):
    def get(self, request, pk):
        medecin = get_object_or_404(Medecin, pk=pk)
        context = {'medecin': medecin}
        return render(request, 'medecins/detail.html', context)
