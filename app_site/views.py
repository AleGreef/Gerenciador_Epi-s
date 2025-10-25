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
    setores = Setor.objects.all()  # Passamos todos os setores para popular o select
    if request.method == 'POST':
        nome_colaborador = request.POST.get('nome_colaborador')
        data_nasc = request.POST.get('data_nasc')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        #id_setor = request.POST.get('setor')
        cpf = request.POST.get('cpf')
        
        #if not id_setor:
            #messages.error(request, "Selecione um setor válido")
            #return render(request, "app_site/pages/cadastrar_colaborador.html", {"setores": setores})

        #setor_obj = Setor.objects.get(id_setor=id_setor)

        # Salva no banco
        Colaboradores.objects.create(
            nome_colaborador=nome_colaborador,
            data_nasc=data_nasc,
            telefone=telefone,
            email=email,
            senha=senha,
            #id_setor=setor_obj,
            cpf=cpf,
            
        )
        messages.success(request, "Colaborador cadastrado com sucesso!")
        return redirect('lista_colaborador')  # Redireciona para a listagem

    return render(request, 'app_site/pages/cadastrar_colaborador.html', {'setores': setores})

def lista_colaborador(request):
    colaboradores = Colaboradores.objects.all()
    return render(request, 'app_site/pages/menu.html', {'colaboradores': colaboradores})
