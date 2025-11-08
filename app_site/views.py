from django.shortcuts import render, redirect
from app_site.models import Colaboradores, Setor, Epis, Emprestimos
from django.contrib import messages
from django import forms
from django.utils import timezone

def cadastrar_equipamento(request):
    return render(request, 'app_site/pages/cadastrar_equipamento.html')

def visualizar_emprestimos(request):
    return render(request, 'app_site/pages/visualizar_emprestimos.html')

def menu(request):
    colaboradores = Colaboradores.objects.filter(delete_flag='N')
    return render(request, 'app_site/pages/menu.html', {'colaboradores': colaboradores})

def cadastrar_colaborador(request):
    setores = Setor.objects.filter(delete_flag='N')

    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome_colaborador = request.POST.get('nome')
        data_nasc = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        foto = request.FILES.get('foto_perfil')

        Colaboradores.objects.create(
            cpf=cpf,
            nome_colaborador=nome_colaborador,
            data_nasc=data_nasc,
            telefone=telefone,
            email=email,
            senha=senha,
            delete_flag='N',
            foto_perfil=foto
        )

        messages.success(request, "Colaborador cadastrado com sucesso!")
        return redirect('lista_colaborador')

    return render(request, 'app_site/pages/cadastrar_colaborador.html', {'setores': setores})

def lista_colaborador(request):
    colaboradores = Colaboradores.objects.filter(delete_flag='N')
    return render(request, 'app_site/pages/menu.html', {'colaboradores': colaboradores})

def login(request):
    return render(request, 'app_site/pages/login.html')

def perfil(request):
    return render(request, 'app_site/pages/perfil.html')

# --- Parte nova para cadastrar reserva ---
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Emprestimos
        fields = ['colaborador', 'epis', 'data_emprestimo', 'data_devolucao', 'status']

def cadastrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            if not reserva.data_emprestimo:
                reserva.data_emprestimo = timezone.now()
            reserva.save()
            messages.success(request, "Reserva cadastrada com sucesso!")
            return redirect('menu')
    else:
        form = ReservaForm()
    return render(request, 'app_site/pages/cadastrar_reserva.html', {'form': form})
