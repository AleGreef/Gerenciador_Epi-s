from django.shortcuts import render, redirect
from app_site.models import Colaboradores, Setor
from django.contrib import messages



def cadastrar_equipamento(request):
    return render(request, 'app_site/pages/cadastrar_equipamento.html')

def visualizar_emprestimos(request):
    return render(request, 'app_site/pages/visualizar_emprestimos.html')

def menu(request):
    return render(request, 'app_site/pages/menu.html')  # 'menu.html' é o template da tela do menu

def cadastrar_colaborador(request):
    setores = Setor.objects.filter(delete_flag='N')  # se depois quiser usar setor

    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome_colaborador = request.POST.get('nome')
        data_nasc = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        Colaboradores.objects.create(
            cpf=cpf,
            nome_colaborador=nome_colaborador,
            data_nasc=data_nasc,
            telefone=telefone,
            email=email,
            senha=senha,
            delete_flag='N'
        )

        messages.success(request, "Colaborador cadastrado com sucesso!")
        return redirect('lista_colaborador')

    return render(request, 'app_site/pages/cadastrar_colaborador.html', {'setores': setores})

def lista_colaborador(request):
    colaboradores = Colaboradores.objects.all()
    return render(request, 'app_site/pages/menu.html', {'colaboradores': colaboradores})
