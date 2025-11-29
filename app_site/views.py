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

        # ===========================
        # EXCLUIR — IGNORA TODO O RESTO
        # ===========================
        if acao == "excluir":
            if id_reserva:
                Reservas.objects.filter(id_reserva=id_reserva).update(delete_flag='S')
                messages.success(request, "Reserva excluída com sucesso.")
            else:
                messages.error(request, "Nenhuma reserva selecionada para excluir.")
            return redirect('realizar_reserva')
        # ===========================

        # A partir daqui é SALVAR / EDITAR
        colaborador_id = request.POST.get('colaborador')
        epi_id = request.POST.get('epi')

        quantidade = int(request.POST.get('quantidade'))
        data_retirada = request.POST.get('data_retirada')
        data_devolucao = request.POST.get('data_devolucao')
        status = request.POST.get('status')

        colaborador = Colaboradores.objects.get(id_col=colaborador_id)
        epi = Epis.objects.get(id_epis=epi_id)

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
def Relatorio(request):
    from django.db.models import Q
    from datetime import date
    
    # Busca todas as reservas ativas
    reservas_query = Reservas.objects.filter(delete_flag='N').order_by('-data_retirada')
    
    # Filtro de busca por nome ou CPF
    busca = request.GET.get('busca', '')
    if busca:
        # Busca colaboradores que correspondem
        colaboradores_encontrados = Colaboradores.objects.filter(
            Q(nome_colaborador__icontains=busca) | 
            Q(cpf__icontains=busca),
            delete_flag='N'
        ).values_list('cpf', flat=True)
        
        reservas_query = reservas_query.filter(cpf__in=colaboradores_encontrados)
    
    # Filtro de status
    status_filtro = request.GET.get('status', '')
    if status_filtro:
        reservas_query = reservas_query.filter(status=status_filtro)
    
    # Monta lista com dados completos
    reservas_lista = []
    for reserva in reservas_query:
        # Busca colaborador
        colaborador = Colaboradores.objects.filter(cpf=reserva.cpf).first()
        
        # Busca EPI
        epi = Epis.objects.filter(id_epis=reserva.cod_epi).first()
        
        # Calcula dias pendentes - INCLUINDO RESERVADO
        dias_pendente = 0
        if reserva.status.lower() in ['pendente', 'reservado', 'emprestado', 'ativo']:
            dias_pendente = (date.today() - reserva.data_retirada).days
        
        reservas_lista.append({
            'id': reserva.id_reserva,
            'colaborador_nome': colaborador.nome_colaborador if colaborador else 'N/A',
            'colaborador_cpf': colaborador.format_cpf() if colaborador else reserva.cpf,
            'epi_nome': epi.nome_epi if epi else 'N/A',
            'epi_tipo': epi.tipo_acessorio if epi else '',
            'quantidade': reserva.quantidade,
            'data_retirada': reserva.data_retirada,
            'data_devolucao': reserva.data_devolucao,
            'status': reserva.status,
            'dias_pendente': dias_pendente
        })
    
    # Estatísticas - INCLUINDO RESERVADO
    total_reservas = Reservas.objects.filter(delete_flag='N').count()
    total_pendentes = Reservas.objects.filter(
        delete_flag='N',
        status__in=['pendente', 'reservado', 'emprestado', 'ativo']
    ).count()
    total_devolvidos = Reservas.objects.filter(
        delete_flag='N',
        status__in=['devolvido', 'finalizado']
    ).count()
    
    context = {
        'reservas': reservas_lista,
        'busca': busca,
        'status': status_filtro,
        'total_reservas': total_reservas,
        'total_pendentes': total_pendentes,
        'total_devolvidos': total_devolvidos,
    }
    
    return render(request, 'app_site/pages/relatorio.html', context)