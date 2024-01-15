# consultas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar_paciente/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('marcar_consulta/', views.marcar_consulta, name='marcar_consulta'),
    path('cancelar_consulta/', views.cancelar_consulta, name='cancelar_consulta'),
]
