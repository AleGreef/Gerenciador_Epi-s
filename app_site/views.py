from django.shortcuts import render, redirect, get_object_or_404
from app_site.models import Colaboradores, Setor
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from app_site.models import Colaboradores, Setor
from django.views.decorators.csrf import csrf_exempt

def cadastrar_equipamento(request):
    return render(request, 'app_site/pages/cadastrar_equipamento.html')

def visualizar_emprestimos(request):
    return render(request, 'app_site/pages/visualizar_emprestimos.html')

def menu(request):
    return render(request, 'app_site/pages/menu.html')  # 'menu.html' é o template da tela do menu

def cadastrar_colaborador(request):
    setores = Setor.objects.filter(delete_flag='N')

    # Valores padrão para repassar ao template
    context = {
        'setores': setores,
        'cpf': '',
        'nome': '',
        'data_nascimento': '',
        'telefone': '',
        'email': '',
        'senha': ''
    }

    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # mantém os valores no contexto
        context.update({
            'cpf': cpf,
            'nome': nome,
            'data_nascimento': data_nascimento,
            'telefone': telefone,
            'email': email,
            'senha': senha
        })

        # verifica duplicidade de CPF
        if Colaboradores.objects.filter(cpf=cpf).exists():
            messages.error(request, "Erro: Já existe um colaborador cadastrado com este CPF.")
        else:
            try:
                Colaboradores.objects.create(
                    cpf=cpf,
                    nome_colaborador=nome,
                    data_nasc=data_nascimento,
                    telefone=telefone,
                    email=email,
                    senha=senha,
                    delete_flag='N'
                )
                messages.success(request, "Colaborador cadastrado com sucesso!")
            except IntegrityError:
                messages.error(request, "Erro ao salvar o colaborador.")

    return render(request, 'app_site/pages/cadastrar_colaborador.html', context)


def lista_colaborador(request):
    colaboradores = Colaboradores.objects.all()
    return render(request, 'app_site/pages/menu.html', {'colaboradores': colaboradores})

def verificar_cpf(request):
    """Consulta AJAX: retorna dados do colaborador se o CPF já existir"""
    cpf = request.GET.get('cpf')
    colaborador = Colaboradores.objects.filter(cpf=cpf).first()

    if colaborador:
        data = {
             'exists': True,
              'colaborador': { 
                'nome_colaborador': colaborador.nome_colaborador,
                'data_nasc': colaborador.data_nasc.strftime("%Y-%m-%d") if colaborador.data_nasc else '',
                'telefone': colaborador.telefone,
                'email': colaborador.email,
                'senha': colaborador.senha,
        }
    }
    else:
        data = {'exists': False}

    return JsonResponse(data)

def gerenciar_colaboradores(request): 
    colaboradores = Colaboradores.objects.all()
    return render(request, 'app_site/pages/gerenciar_colaboradores.html', {'Colaboradores': colaboradores})

def editar_colaboradores(request, id):
    colaborador = get_object_or_404(Colaboradores, id=id)

    if request.method == 'POST':
        colaborador.cpf = request.POST.get('cpf')
        colaborador.nome_colaborador = request.POST.get('nome_colaborador')
        colaborador.data_nasc = request.POST.get('data_nasc')
        colaborador.telefone = request.POST.get('telefone')
        colaborador.email = request.POST.get('email')
        colaborador.senha = request.POST.get('senha')  # ⚠️ use hashing em produção
        colaborador.save()

        messages.success(request, 'Colaborador atualizado com sucesso!')
        return redirect('gerenciar_colaboradores')

    return render(request, 'app_site/pages/editar_colaborador.html', {'colaborador': colaborador})


def excluir_colaborador(request):
    return render(request, 'app_site/pages/excluir_colaborador.html')
