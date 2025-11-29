from django.shortcuts import render, redirect, get_object_or_404
from app_site.models import Colaboradores, Epis, Setor
from app_login.models import CustomUser
from django.db import transaction
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import  HttpRequest

User = CustomUser

@login_required(login_url='accounts:login')
def cadastrar_equipamento(request):

    if request.method == 'POST':
        nome_epi = request.POST.get('nome_epi')
        fabricante = request.POST.get('fabricante')
        tipo_acessorio = request.POST.get('tipo_acessorio')
        data_validade = request.POST.get('data_validade')
        tamanho = request.POST.get('tamanho')
        qtd_estoque = request.POST.get('qtd_estoque')

         # Salva no banco
        Epis.objects.create(
            nome_epi = nome_epi,
            fabricante = fabricante,
            tipo_acessorio= tipo_acessorio,
            data_validade = data_validade,
            tamanho=tamanho,
            qtd_estoque = qtd_estoque,
            delete_flag='N',
        )
  
        messages.success(request, '✅ Equipamento cadastrado com sucesso!')
        return redirect('colaboradores:cadastrar_equipamento')  # ou a página que você quiser
          
    return render(request, 'app_site/pages/cadastrar_equipamento.html')

@login_required(login_url='accounts:login')
def listar_emprestimos(request):
    return render(request, 'app_site/pages/listar_emprestimos.html')

@login_required(login_url='accounts:login')
def menu(request):
    return render(request, 'app_site/pages/menu.html')  # 'menu.html' é o template da tela do menu

@login_required(login_url='accounts:login')
def cadastrar_colaborador(request):

    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome_colaborador = request.POST.get('nome_colaborador')
        data_nasc = request.POST.get('data_nasc')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        foto = request.FILES.get('foto_perfil')

         # Verifica se o cpf já existe
        if Colaboradores.objects.filter(cpf=cpf).exists():
            messages.error(request, "Este usuário já está em uso. Escolha outro.")
            return redirect("colaboradores:cadastrar_colaborador")

        # converter data
        if data_nasc:
            data_nasc = datetime.strptime(data_nasc, "%Y-%m-%d").date() if data_nasc else None
        else:
            data_nasc = None
       
        try:
            
            user = User.objects.create_user(
                email=email,
                password=senha,
                cpf=cpf,
            )
            Colaboradores.objects.create(
                user=user,
                cpf=cpf,
                nome_colaborador=nome_colaborador,
                data_nasc=data_nasc,
                telefone=telefone,
                email=email,
                senha=senha,
                tipo_colaborador='usuario',
                delete_flag='N',
                foto_perfil=foto
            )
        except Exception as e:
            messages.error(request, f"Erro ao finalizar o cadastro: {e}")
            return redirect("colaboradores:cadastrar_colaborador")
        messages.success(request, "Colaborador cadastrado com sucesso!")
        return redirect('colaboradores:cadastrar_colaborador')
    return render(request, 'app_site/pages/cadastrar_colaborador.html')

@login_required(login_url='accounts:login')
def listar_colaborador(request):
    pesquisa = request.GET.get("nome_colaborador", "")  # pega o texto digitado
    if pesquisa:
        colaboradores = Colaboradores.objects.filter(
            nome_colaborador__icontains=pesquisa,
            cpf__icontains=pesquisa
        )
    else:
        colaboradores = Colaboradores.objects.all()

    return render(request, "app_site/pages/listar_colaborador.html", {
        "colaboradores": colaboradores,
        "pesquisa": pesquisa
    })

@login_required(login_url='accounts:login')
def listar_equipamentos(request):
    pesquisa = request.GET.get("nome_epi", "")
    if pesquisa:
        epis = Epis.objects.filter(
            nome_epi__icontains=pesquisa
        )
    else:    
        epis = Epis.objects.all()

    return render(request, 'app_site/pages/listar_equipamentos.html', {
        "epis": epis,
        "pesquisa": pesquisa
        })

@login_required(login_url='accounts:login')
def listar_setor(request):
    pesquisa = request.GET.get("nome_setor", "")
    if pesquisa:
        setor = Setor.objects.filter(
            nome_setor__icontains=pesquisa
        )
    else:
        setor = Setor.objects.all()
    
    return render(request, 'app_site/pages/listar_setor.html', {
        "setor": setor,
        "pesquisa": pesquisa
        })

@login_required(login_url='accounts:login')
def remover_colaborador(request, id:int):
# Garante que se uma exclusão falhar, a outra também será revertida.
    try:
        with transaction.atomic():
            # A. Encontra o registro auxiliar (Colaboradores)
            colaborador_aux = get_object_or_404(Colaboradores, id_col=id)
            
            # B. Obtém o e-mail para encontrar o usuário principal
            email_colaborador = colaborador_aux.email
            nome_colaborador = colaborador_aux.nome_colaborador

            # C. Encontra e exclui o CustomUser (usuário logável)
            try:
                # 🚨 Esta exclusão remove o registro da tabela app_login_customuser
                user_principal = CustomUser.objects.get(email=email_colaborador)
                user_principal.delete()
            except CustomUser.DoesNotExist:
                # Isso impede que o processo falhe caso o CustomUser já tenha sido deletado
                pass 
                
            # D. Exclui o registro auxiliar (Colaboradores)
            # Esta exclusão também removerá registros em tabelas que fazem Foreign Key para Colaboradores (ex: Emprestimos)
            colaborador_aux.delete()
            
            messages.success(request, f"Colaborador {nome_colaborador} excluído com sucesso (incluindo usuário principal).")

    except Exception as e:
        messages.error(request, f"Erro ao excluir o colaborador: {e}")
        # O Django irá reverter as operações dentro do bloco 'with transaction.atomic()' se ocorrer um erro.

    return redirect('colaboradores:listar_colaborador')

@login_required(login_url='accounts:login')
def remover_equipamento(request, id:int):
# Garante que se uma exclusão falhar, a outra também será revertida.
    try:
        with transaction.atomic():
            # A. Encontra o registro auxiliar (Epis)
            equipamento_aux = get_object_or_404(Epis, id_epis=id)
            
            # B. Obtém o e-mail para encontrar o usuário principal
            nome_epi = equipamento_aux.nome_epi

            equipamento_aux.delete()
            
            messages.success(request, f"Equipamento {nome_epi} excluído com sucesso.")

    except Exception as e:
        messages.error(request, f"Erro ao excluir o equipamento: {e}")

    return redirect('colaboradores:listar_equipamentos')

@login_required(login_url='accounts:login')
def remover_setor(request, id:int):
# Garante que se uma exclusão falhar, a outra também será revertida.
    try:
        with transaction.atomic():
            # A. Encontra o registro auxiliar (Setor)
            setor_aux = get_object_or_404(Setor, id_setor=id)
            
            # B. Obtém o e-mail para encontrar o usuário principal
            nome_setor = setor_aux.nome_setor

            setor_aux.delete()
            
            messages.success(request, f"Setor {nome_setor} excluído com sucesso.")

    except Exception as e:
        messages.error(request, f"Erro ao excluir setor: {e}")

    return redirect('colaboradores:listar_setor')

@login_required(login_url='accounts:login')
def editar_colaborador(request: HttpRequest, id: int):
    colaborador = get_object_or_404(Colaboradores, id_col=id)

    if request.method == 'POST':
        try:
            colaborador.nome_colaborador = request.POST.get('nome_colaborador')
            colaborador.data_nasc = request.POST.get('data_nasc')
            colaborador.telefone = request.POST.get('telefone')
            colaborador.senha = request.POST.get('senha')
            colaborador.email = request.POST.get('email')
            colaborador.cpf = request.POST.get('cpf')

            # Foto só atualiza se o usuário enviar
            foto = request.FILES.get('foto_perfil')
            if foto:
                colaborador.foto_perfil = foto

            colaborador.save()

            messages.success(request, '✅ Colaborador atualizado com sucesso!')
            return redirect('colaboradores:listar_colaborador')
        except Exception:
            print("ERRO AO ATUALIZAR:")
            messages.error(request, "❌ Não foi possível atualizar o colaborador. Tente novamente.")
            return redirect('colaboradores:editar_colaborador', id=id)
        
    return render(request, 'app_site/pages/cadastrar_colaborador.html', {
        'colaborador': colaborador,
        'modo_edicao': True
    })

@login_required(login_url='accounts:login')
def editar_equipamento(request: HttpRequest, id: int):
    equipamento = get_object_or_404(Epis, id_epis=id)

    if request.method == 'POST':
        try:
            equipamento.nome_epi = request.POST.get('nome_epi')
            equipamento.tipo_acessorio = request.POST.get('tipo_acessorio')
            equipamento.fabricante = request.POST.get('fabricante')
            equipamento.data_validade = request.POST.get('data_validade')
            equipamento.tamanho = request.POST.get('tamanho')
            equipamento.qtd_estoque = request.POST.get('qtd_estoque')

            equipamento.save()

            messages.success(request, '✅ Equipamento atualizado com sucesso!')
            return redirect('colaboradores:listar_equipamentos')
        except Exception:
            print("ERRO AO ATUALIZAR:")
            messages.error(request, "❌ Não foi possível atualizar o equipamento. Tente novamente.")
            return redirect('colaboradores:editar_equipamento', id=id)
        
    return render(request, 'app_site/pages/cadastrar_equipamento.html', {
        'equipamento': equipamento,
        'modo_edicao': True,
    })

@login_required(login_url='accounts:login')
def editar_setor(request: HttpRequest, id: int):
    setor = get_object_or_404(Setor, id_setor=id)

    if request.method == 'POST':
        try:
            setor.nome_setor = request.POST.get('nome_setor')
            setor.epis_necessario = request.POST.get('epis_necessario')

            setor.save()

            messages.success(request, '✅ Setor atualizado com sucesso!')
            return redirect('colaboradores:listar_setor')
        except Exception:
            print("ERRO AO ATUALIZAR:")
            messages.error(request, "❌ Não foi possível atualizar o setor. Tente novamente.")
            return redirect('colaboradores:editar_setor', id=id)
        
    return render(request, 'app_site/pages/cadastrar_setor.html', {
        'setor': setor,
        'modo_edicao': True,
    })

@login_required(login_url='accounts:login')
def perfil(request):
    # Busca o colaborador relacionado ao usuário logado
    try:
        colaborador = Colaboradores.objects.get(user=request.user)
    except Colaboradores.DoesNotExist:
        messages.error(
            request,
            "Seu perfil ainda não foi configurado. Complete suas informações."
        )
        return redirect('colaboradores:cadastrar_colaborador')

    # Debug profissional
    print("=== DEBUG PERFIL ===")
    print("Usuário logado:", request.user.username)
    print("Colaborador encontrado:", colaborador)
    print("Nome:", colaborador.nome_colaborador)
    print("Email:", colaborador.email)
    print("Foto:", colaborador.foto_perfil)

    return render(request, "app_site/pages/perfil.html", {
        "colaborador": colaborador
    })

def cadastrar_setor(request):
    if request.method == 'POST':
        nome_setor = request.POST.get('nome_setor')
        epis_necessario = request.POST.get('epis_necessario')

        if nome_setor:
            Setor.objects.create(
                nome_setor = nome_setor,
                epis_necessario=epis_necessario,
                delete_flag='N',   
            )
            messages.success(request, '✅ Setor cadastrado com sucesso!')
            return redirect('colaboradores:cadastrar_setor')  # ou a página que você quiser
        else:
            messages.error(request, '❌ Não foi possivel cadastrar o setor!')

    return render(request, 'app_site/pages/cadastrar_setor.html')

@login_required(login_url='accounts:login')
def realizar_emprestimo(request):
    return render(request, 'app_site/pages/realizar_emprestimo.html')



