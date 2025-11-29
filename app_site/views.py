from django.shortcuts import render, redirect, get_object_or_404
from app_site.models import Colaboradores, Epis, Setor, Emprestimos
from app_login.models import CustomUser
from django.db import transaction
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import  HttpRequest
from django.http import JsonResponse
from django.db import IntegrityError


User = CustomUser


@login_required(login_url='accounts:login')
def buscar_equipamentos(request):
    term = request.GET.get('term', '')
    epis = Epis.objects.filter(nome_epi__icontains=term)
    # Retorna como array de objetos
    data = [{"id": e.id_epis, "text": e.nome_epi} for e in epis]
    return JsonResponse(data, safe=False)  # safe=False porque é uma lista

@login_required(login_url='accounts:login')
def buscar_colaboradores(request):
    term = request.GET.get('term', '')
    # O filtro icontains está correto para a busca
    colaboradores = Colaboradores.objects.filter(nome_colaborador__icontains=term)

    # 🚨 Mude 'id_col' para 'id'
    data = [{"id": c.id_col, "text": c.nome_colaborador} for c in colaboradores]
    
    return JsonResponse(data, safe=False)

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

def listar_emprestimos(request):
    # Inicializa o QuerySet com todos os empréstimos ativos (delete_flag='N')
    emprestimos = Emprestimos.objects.filter(delete_flag='N')
    
    # Dicionário para armazenar os filtros e enviar de volta ao template
    filtros = {}

    # --- 1. FILTRO POR NOME DO COLABORADOR ---
    colaborador_nome = request.GET.get('colaborador_nome')
    if colaborador_nome:
        # Usa __icontains para buscar parte do nome, ignorando case
        emprestimos = emprestimos.filter(
            colaborador__nome_colaborador__icontains=colaborador_nome
        )
        filtros['colaborador_nome'] = colaborador_nome

    # --- 2. FILTRO POR NOME DO EQUIPAMENTO (EPI) ---
    equipamento_nome = request.GET.get('equipamento_nome')
    if equipamento_nome:
        # Usa __icontains para buscar parte do nome, ignorando case
        emprestimos = emprestimos.filter(
            epis__nome_epi__icontains=equipamento_nome
        )
        filtros['equipamento_nome'] = equipamento_nome

    # --- 3. FILTRO POR STATUS ---
    status = request.GET.get('status')
    if status:
        # Usa __iexact (igualdade exata, ignorando case) para o status
        emprestimos = emprestimos.filter(
            status__iexact=status
        )
        filtros['status'] = status
        
    # Os filtros acima são combinados automaticamente por Django com o operador AND.
    # Exemplo: (colaborador__icontains) AND (epis__icontains) AND (status__iexact)

    context = {
        'emprestimos': emprestimos,
        'filtros': filtros # Envia os filtros de volta para preencher o formulário no template
    }
    
    return render(request, "app_site/pages/listar_emprestimos.html", context)
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
def remover_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimos, pk=pk)

    if request.method == "POST":
        emprestimo.delete()
        messages.success(request, "Empréstimo excluído com sucesso!")
        return redirect("colaboradores:listar_emprestimos")

    return redirect("colaboradores:listar_emprestimos")

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
def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimos, id=id)

    if request.method == "POST":
        # 1. Coletar e tratar campos editáveis
        status_post = request.POST.get("status")
        data_devolver_post = request.POST.get("data_devolver")
        observacoes_post = request.POST.get("observacoes")

        # --- A. Tratamento da Data de Devolução ---
        data_devolver_obj = None
        if data_devolver_post and data_devolver_post != '':
            try:
                # Converte para objeto date
                data_devolver_obj = datetime.strptime(data_devolver_post, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Formato de Data de Devolução inválido. Use YYYY-MM-DD.")
                # 🚨 CORREÇÃO: Redireciona para a mesma página de edição (com o ID)
                return redirect("colaboradores:editar_emprestimo", id=id)

        # --- B. Tratamento de Observações ---
        if observacoes_post == '':
            observacoes_post = None

        # --- C. ATUALIZAÇÃO DO OBJETO ---
        emprestimo.status = status_post
        emprestimo.data_devolver = data_devolver_obj
        emprestimo.observacao = observacoes_post 
        
        try:
            emprestimo.save() 
            messages.success(request, "Empréstimo atualizado com sucesso!")
            # Redireciona para a lista (Sucesso)
            return redirect("colaboradores:listar_emprestimos")
        
        except IntegrityError as e:
            messages.error(request, f"Erro de integridade ao salvar: {e}. Verifique se todos os campos obrigatórios foram preenchidos corretamente.")
            # 🚨 CORREÇÃO: Redireciona para a mesma página de edição (com o ID)
            return redirect("colaboradores:editar_emprestimo", id=id)
        except Exception as e:
            messages.error(request, f"Ocorreu um erro inesperado: {e}")
            # 🚨 CORREÇÃO: Redireciona para a mesma página de edição (com o ID)
            return redirect("colaboradores:editar_emprestimo", id=id)
        
    # GET request
    context = {
        'emprestimo': emprestimo,
        'colaborador_atual': emprestimo.colaborador, 
        'equipamento_atual': emprestimo.epis,        
        'modo_edicao': True                         
    }
    # O caminho do template está correto: "app_site/pages/realizar_emprestimo.html"
    return render(request, "app_site/pages/realizar_emprestimo.html", context)

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

@login_required(login_url='accounts:login')
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
    if request.method == "POST":
        # 1. Coleta e Limpeza dos dados
        
        # Campos obrigatórios (presume-se)
        colaborador_id = request.POST.get("nome_colaborador")
        epis_id = request.POST.get("nome_epi")
        data_emprestimo = request.POST.get("data_emprestimo") # Deve ser YYYY-MM-DD
        data_prevista = request.POST.get("data_prevista")     # Deve ser YYYY-MM-DD
        status = request.POST.get("status")

        # Campos opcionais que precisam ser tratados para evitar string vazia ('')
        data_devolver = request.POST.get("data_devolver")
        observacoes = request.POST.get("observacoes")

        # 2. Tratamento do campo 'data_devolver' (O MAIS IMPORTANTE)
        # Se o campo vier vazio (''), o Django tenta converter em DateTime e falha.
        # Devemos forçar que seja None se estiver vazio, para que o campo seja NULL no DB.
        if data_devolver == '':
            data_devolver = None
            
        # O mesmo para observacoes
        if observacoes == '':
            observacoes = None

        try:
            # 3. Busca os objetos corretos
            colaborador = Colaboradores.objects.get(id_col=colaborador_id)
            equipamento = Epis.objects.get(id_epis=epis_id)

            # 4. Cria o registro
            Emprestimos.objects.create(
                colaborador=colaborador,
                epis=equipamento,
                data_emprestimo=data_emprestimo,
                data_prevista=data_prevista,
                # O valor agora é 'None' se estiver vazio, o que resolve o erro
                data_devolver=data_devolver, 
                status=status,
                observacao=observacoes, # Garantindo que observacoes seja passado
                delete_flag='N',
            )

            messages.success(request, "Empréstimo registrado com sucesso!")
            return redirect("colaboradores:listar_emprestimos")
        
        except Colaboradores.DoesNotExist:
             messages.error(request, "Colaborador não encontrado.")
             # Adicione um retorno para evitar falha
             return redirect("colaboradores:realizar_emprestimo") 
        except Epis.DoesNotExist:
             messages.error(request, "Equipamento não encontrado.")
             # Adicione um retorno para evitar falha
             return redirect("colaboradores:realizar_emprestimo")
        except Exception as e:
            # Captura outros erros de criação, como formato de data inválido para campos obrigatórios
            messages.error(request, f"Erro ao registrar empréstimo: {e}")
            return redirect("colaboradores:realizar_emprestimo")

    # 5. Renderiza o formulário (GET request)
    return render(request, "app_site/pages/realizar_emprestimo.html")

@login_required(login_url='accounts:login')
def relatorios(request):
    return render(request, 'app_site/pages/relatorios.html')