from django.shortcuts import render, redirect, get_object_or_404
from app_site.models import Colaboradores, Setor
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from app_site.models import Colaboradores, Setor
from django.views.decorators.csrf import csrf_exempt
from .models import Epis
from .models import Colaboradores, Epis, Reservas
from django.contrib import messages
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Colaboradores, Epis, Reservas



def cadastrar_equipamento(request):
    return render(request, 'app_site/pages/cadastrar_equipamento.html')

def visualizar_emprestimos(request):
    return render(request, 'app_site/pages/visualizar_emprestimos.html')

def menu(request):
    colaboradores = Colaboradores.objects.all()
    return render(request, 'app_site/pages/menu.html', {
        'colaboradores': colaboradores
    })

def cadastrar_colaborador(request):
    setores = Setor.objects.filter(delete_flag='N')

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

        # mantém valores preenchidos na tela
        context.update({
            'cpf': cpf,
            'nome': nome,
            'data_nascimento': data_nascimento,
            'telefone': telefone,
            'email': email,
            'senha': senha
        })

        # verifica duplicidade
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
                # NÃO faz redirect — permanece na página com dados preenchidos

            except IntegrityError:
                messages.error(request, "Erro ao salvar o colaborador.")

    return render(request, 'app_site/pages/cadastrar_colaborador.html', context)

def lista_colaborador(request):
    colaboradores = Colaboradores.objects.all()
    return render(request, 'app_site/pages/menu.html', {'colaboradores': colaboradores})

def login(request):
    return render(request, 'app_site/pages/login.html')

def perfil(request):
    return render(request, 'app_site/pages/perfil.html')
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

def editar_colaborador(request, cpf):
    colaborador = get_object_or_404(Colaboradores, cpf=cpf)
    setores = Setor.objects.filter(delete_flag='N')

    if request.method == 'POST':
        colaborador.nome_colaborador = request.POST.get('nome')
        colaborador.data_nasc = request.POST.get('data_nascimento')
        colaborador.telefone = request.POST.get('telefone')
        colaborador.email = request.POST.get('email')
        colaborador.senha = request.POST.get('senha')
        colaborador.save()

        messages.success(request, "Colaborador atualizado.")
        return redirect('menu')

    return render(request, 'app_site/pages/cadastrar_colaborador.html', {
        'colaborador': colaborador,
        'setores': setores,
        'modo_edicao': True
    })

def excluir_colaborador(request):
    if request.method == "POST":
        cpf = request.POST.get("cpf")

        if cpf:
            Colaboradores.objects.filter(cpf=cpf).delete()

        return redirect('menu')
    
def cadastrar_equipamento(request):
    equipamentos = Epis.objects.all().order_by('-id_epis')

    if request.method == "POST":
        nome = request.POST.get("nome_epi")
        fabricante = request.POST.get("fabricante")
        tamanho = request.POST.get("tamanho")
        tipo = request.POST.get("tipo_acessorio")
        saldo = request.POST.get("saldo")
        emprestado = request.POST.get("emprestado")

        Epis.objects.create(
            nome_epi=nome,
            fabricante=fabricante,
            tamanho=tamanho,
            tipo_acessorio=tipo,
            saldo=saldo,
            emprestado=emprestado,
            delete_flag="N"
        )

        return redirect('cadastrar_equipamento')

    return render(request, "app_site/pages/cadastrar_equipamento.html", {
        'equipamentos': equipamentos
    })


def realizar_reserva(request):
    colaboradores = Colaboradores.objects.filter(delete_flag='N')
    epis = Epis.objects.filter(delete_flag='N')
    reservas = Reservas.objects.filter(delete_flag='N')

    if request.method == "POST":
        acao = request.POST.get("acao")
        id_reserva = request.POST.get("id_reserva")

        # EXCLUIR
        if acao == "excluir" and id_reserva:
            Reservas.objects.filter(id_reserva=id_reserva).update(delete_flag='S')
            messages.success(request, "Reserva excluída com sucesso.")
            return redirect('realizar_reserva')

        # SALVAR / ATUALIZAR
        colaborador_id = request.POST.get('colaborador')
        epi_id = request.POST.get('epi')

        # VALIDAÇÕES IMPORTANTES
        if not colaborador_id:
            messages.error(request, "Selecione um colaborador antes de salvar.")
            return redirect('realizar_reserva')

        if not epi_id:
            messages.error(request, "Selecione um EPI antes de salvar.")
            return redirect('realizar_reserva')

        quantidade = int(request.POST.get('quantidade'))
        data_retirada = request.POST.get('data_retirada')
        data_devolucao = request.POST.get('data_devolucao')
        status = request.POST.get('status')

        # Buscar objetos
        try:
            colaborador = Colaboradores.objects.get(id_col=colaborador_id)
        except Colaboradores.DoesNotExist:
            messages.error(request, "Colaborador não encontrado!")
            return redirect('realizar_reserva')

        try:
            epi = Epis.objects.get(id_epis=epi_id)
        except Epis.DoesNotExist:
            messages.error(request, "EPI não encontrado!")
            return redirect('realizar_reserva')

        # NOVA RESERVA
        if not id_reserva:
            Reservas.objects.create(
                cpf=colaborador.cpf,
                cod_epi=epi.id_epis,
                quantidade=quantidade,
                data_retirada=data_retirada,
                data_devolucao=data_devolucao,
                status=status
            )
            messages.success(request, "Reserva cadastrada com sucesso!")

        # ATUALIZAR RESERVA
        else:
            Reservas.objects.filter(id_reserva=id_reserva).update(
                cpf=colaborador.cpf,
                cod_epi=epi.id_epis,
                quantidade=quantidade,
                data_retirada=data_retirada,
                data_devolucao=data_devolucao,
                status=status
            )
            messages.success(request, "Reserva atualizada com sucesso!")

        return redirect('realizar_reserva')

    return render(request, "app_site/pages/realizar_reserva.html", {
        "colaboradores": colaboradores,
        "epis": epis,
        "reservas": reservas,
    })
