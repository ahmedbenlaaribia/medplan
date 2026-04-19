from django.urls import path
from .views import MedecinListView, MedecinDetailView

urlpatterns = [
    path('', MedecinListView.as_view(), name='medecins_list'),
    path('<int:pk>/', MedecinDetailView.as_view(), name='medecin_detail'),
]