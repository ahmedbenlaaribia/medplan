from django.urls import path
from .views import RendezVousListView, RendezVousCreateView

urlpatterns = [
    path('', RendezVousListView.as_view(), name='rdv_list'),
    path('nouveau/<int:medecin_id>/', RendezVousCreateView.as_view(), name='rdv_create'),
]