from django.shortcuts import render
from consultas import views
from consultas.views import index

from django.urls import path

def index(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', index, name='index'),
    path('cadastrar_paciente/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('marcar_consulta/', views.marcar_consulta, name='marcar_consulta'),
    path('cancelar_consulta/', views.cancelar_consulta, name='cancelar_consulta'),
]