from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cartoes, name='lista_cartoes'),
]