# consultas/models.py
from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, unique=True)

class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    dia = models.DateField()
    hora = models.TimeField()
    especialidade = models.CharField(max_length=255)

    class Meta:
        app_label = 'consultas'
