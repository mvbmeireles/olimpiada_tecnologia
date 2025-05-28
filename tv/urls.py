from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cartoes, name='lista_cartoes'),
    path('detalhes/<int:projeto_id>/', views.detalhes_projeto, name='detalhes_projeto'),
    path('api/add_repair_step/', views.add_repair_step, name='add_repair_step'),
    path('api/update_repair_step_status/', views.update_repair_step_status, name='update_repair_step_status'),
]