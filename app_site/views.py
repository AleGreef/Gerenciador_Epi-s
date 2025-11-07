from django.shortcuts import render, redirect
from app_site.models import Colaboradores, Setores, Equipamentos
from django.contrib import messages
from django.http import  HttpRequest
from django.contrib.auth.models import User

def remover_colaborador(request: HttpRequest):
    raise NotImplementedError

def editar_colaborador(request: HttpRequest):
    raise NotImplementedError

def cadastrar_equipamento(request):
    if request.method == 'POST':
        nome_equipamento = request.POST.get('nome_equipamento')
        fabricante = request.POST.get('fabricante')
        data_validade = request.POST.get('data_validade')
        estoque = request.POST.get('estoque')

         # Salva no banco
        Equipamentos.objects.create(
            nome_equipamento = nome_equipamento,
            fabricante = fabricante,
            data_validade = data_validade,
            estoque = estoque,
        )

        if nome_equipamento:
            Equipamentos.objects.create(nome=nome_equipamento)
            messages.success(request, '✅ Equipamento cadastrado com sucesso!')
            return redirect('listar_equipamentos')  # ou a página que você quiser
        else:
            messages.error(request, '❌ Não foi possivel cadastrar o equipamento!')
    
    return render(request, 'app_site/pages/cadastrar_equipamento.html')

def visualizar_emprestimos(request):
    return render(request, 'app_site/pages/visualizar_emprestimos.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return redirect('login_view')

        try:
            colaborador = Colaboradores.objects.get(email=email, senha=senha)
            # Salva o ID na sessão
            request.session['colaborador_id'] = colaborador.id_col
            request.session['colaborador_nome'] = colaborador.nome_Colaborador
            return redirect('menu')
        except Colaboradores.DoesNotExist:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login_view')

    return render(request, 'app_site/pages/login_view.html')

def listar_equipamentos(request):
    equipamentos = Equipamentos.objects.all()
    return render(request, 'app_site/pages/listar_equipamentos.html', {'equipamentos': equipamentos})

def cadastrar_setor(request):
    if request.method == 'POST':
        nome_setor = request.POST.get('nome_setor')

        Setores.objects.create(
            nome_setor = nome_setor
            
        )

        if nome_setor:
            Setores.objects.create(nome=nome_setor)
            messages.success(request, '✅ Setor cadastrado com sucesso!')
            return redirect('listar_setores')  # ou a página que você quiser
        else:
            messages.error(request, '❌ Não foi possivel cadastrar o setor!')

    return render(request, 'app_site/pages/cadastrar_setor.html')

def listar_setores(request):
    setores = Setores.objects.all()
    return render(request, 'app_site/pages/listar_setores.html', {'setores': setores})

def menu(request):
    if not request.session.get('colaborador_id'):
        return redirect('login_view')

    nome = request.session.get('colaborador_nome')
    return render(request, 'app_site/pages/menu.html', {'nome': nome})

def cadastrar_colaborador(request):

    if request.method == 'POST':
        file = request.FILES.get("foto_perfil")
        
        mf = Colaboradores(foto_perfil=file)
        mf.save()
        nome_Colaborador = request.POST.get('nome_Colaborador')
        Data_nasc = request.POST.get('Data_nasc')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        cpf = request.POST.get('cpf')

        # Salva no banco
        Colaboradores.objects.create(
            nome_Colaborador=nome_Colaborador,
            Data_nasc=Data_nasc,
            telefone=telefone,
            email=email,
            senha=senha,
            cpf=cpf,
            
        )
        if nome_Colaborador:
            Equipamentos.objects.create(nome=nome_Colaborador)
            messages.success(request, '✅ Colaborador cadastrado com sucesso!')
            return redirect('listar_colaborador')  # ou a página que você quiser
        else:
            messages.error(request, '❌ Não foi possivel cadastrar o colaborador!')

    return render(request, 'app_site/pages/cadastrar_colaborador.html')

def listar_colaborador(request):
    colaboradores = Colaboradores.objects.all()
    return render(request, 'app_site/pages/listar_colaborador.html', {'colaboradores': colaboradores})

def esqueceu_senha(request):
    if request.method == 'POST':
        email = request.POST['email']
        if not email:
            messages.error(request, 'Informe seu e-mail.')
            return redirect('esqueceu_senha')

        try:
            user = User.objects.get(email=email)
            messages.success(request, f'Um link de recuperação foi enviado para {email}.')
        except User.DoesNotExist:
            messages.error(request, 'E-mail não encontrado.')

        return redirect('esqueceu_senha')

    return render(request, 'app_site/pages/esqueceu_senha.html')

def logout_view(request):
    # Limpa toda a sessão do usuário
    request.session.flush()
    return redirect('login_view')

def cadastrar_usuario(request):
    return render(request, 'app_site/pages/cadastrar_usuario.html')

def realizar_emprestimos(request):
    return render(request, 'app_site/pages/realizar_emprestimos.html')