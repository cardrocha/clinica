from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import reverse
from .models import Paciente, Agendamento

def index(request):
    storage = get_messages(request)
    storage.used = True

    return render(request, 'index.html')

def cadastrar_paciente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')

        # Verificar se o paciente já está cadastrado
        if Paciente.objects.filter(telefone=telefone).exists():
            link_voltar = reverse('cadastrar_paciente')
            mensagem_ja_cadastrado = f"Paciente já cadastrado! <a href='{link_voltar}'>Voltar</a>"
            return HttpResponse(mensagem_ja_cadastrado)

        # Cadastrar o paciente
        paciente = Paciente(nome=nome, telefone=telefone)
        paciente.save()

        link_voltar = reverse('index')
        mensagem_com_link = f"Paciente cadastrado com sucesso! <a href='{link_voltar}'>Voltar ao Index</a>"

        return HttpResponse(mensagem_com_link)
    else:
        return render(request, 'cadastrar_paciente.html')

def marcar_consulta(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente_id')
        dia = request.POST.get('dia')
        hora = request.POST.get('hora')
        especialidade = request.POST.get('especialidade')

        # Verificar se a data é retroativa
        data_agendamento = datetime.strptime(f"{dia} {hora}", "%Y-%m-%d %H:%M")
        if data_agendamento <= datetime.now():
            link_voltar = reverse('marcar_consulta')
            consulta_ja_cadastrada = f"Não é possível agendar consultas retroativas! <a href='{link_voltar}'>Voltar</a>"
            return HttpResponse(consulta_ja_cadastrada)

        # Verificar se a data e hora estão disponíveis
        if Agendamento.objects.filter(dia=dia, hora=hora).exists():
            link_voltar = reverse('marcar_consulta')
            consulta_ja_cadastrada = f"Horário já agendado. Escolha outro horário! <a href='{link_voltar}'>Voltar</a>"
            return HttpResponse(consulta_ja_cadastrada)

        # Marcar a consulta
        paciente = Paciente.objects.get(id=paciente_id)
        agendamento = Agendamento(paciente=paciente, dia=dia, hora=hora, especialidade=especialidade)
        agendamento.save()
        link_voltar = reverse('index')
        consulta_cadastrada = f"Consulta marcada com sucesso! <a href='{link_voltar}'>Voltar ao menu principal</a>"
        return HttpResponse(consulta_cadastrada)
    else:
        pacientes = Paciente.objects.all()
        return render(request, 'marcar_consulta.html', {'pacientes': pacientes})

def cancelar_consulta(request):
    if request.method == 'POST':
        agendamento_id = request.POST.get('agendamento_id')

        if agendamento_id is not None:
            # Cancelar apenas a consulta selecionada
            agendamento = Agendamento.objects.get(id=agendamento_id)
            agendamento.delete()

            nome_paciente = agendamento.paciente.nome

            link_voltar = reverse('index')
            consulta_cancelada = f"Consulta do {nome_paciente} foi cancelada com sucesso! <a href='{link_voltar}'>Voltar ao menu principal</a>"
            return HttpResponse(consulta_cancelada)
        else:
            return HttpResponse("Selecione uma consulta para cancelar.")
    else:
        agendamentos = Agendamento.objects.all()
        return render(request, 'cancelar_consulta.html', {'agendamentos': agendamentos})

def confirmar_cancelamento(request):
    if request.method == 'POST':
        agendamento_id = request.POST.get('agendamento_id')

        try:
            agendamento = Agendamento.objects.get(id=agendamento_id)
        except Agendamento.DoesNotExist:
            return HttpResponse("Operação de cancelamento não autorizada.")

        # Remover apenas a consulta selecionada
        agendamento.delete()
        return redirect('index')  # Substitua 'nome_da_view_principal' pelo nome real da sua view principal
    else:
        return HttpResponse("Operação de cancelamento não autorizada.")
    