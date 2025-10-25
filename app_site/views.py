from django.shortcuts import render, redirect
from .models import Colaboradores


def cadastrar_equipamento(request):
    return render(request, 'app_site/pages/cadastrar_equipamento.html')

def visualizar_emprestimos(request):
    return render(request, 'app_site/pages/visualizar_emprestimos.html')

def menu(request):
    return render(request, 'app_site/pages/menu.html')  # 'menu.html' é o template da tela do menu

def cadastrar_colaborador(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cargo = request.POST.get('cargo')
        telefone = request.POST.get('telefone')
        data_admissao = request.POST.get('data_admissao')

        # Salva no banco
        Colaboradores.objects.create(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            cargo=cargo,
            telefone=telefone,
            data_admissao=data_admissao
        )

        return redirect('lista_colaborador')  # Redireciona para a listagem

    return render(request, 'cadastrar_colaborador.html')

def lista_colaborador(request):
    colaboradores = Colaboradores.objects.all()
    return render(request, 'lista_colaborador.html', {'colaboradores': colaboradores})
