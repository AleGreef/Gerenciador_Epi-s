from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from app_site.models import Colaboradores
from datetime import datetime
from app_login.models import CustomUser
User = CustomUser

def criar_usuario(request):

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
            return redirect("accounts:criar_usuario")

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
    return render(request, 'app_login/pages/criar_usuario.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        print("Email recebido:", email)
        print("Senha:", senha)

        if not email or not senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return redirect('accounts:login')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Usuário não encontrado!!!")
            return redirect('accounts:login')

         # **Validação direta da senha**
        if not user.check_password(senha):
            messages.error(request, "Usuário ou senha incorretos.")
            return redirect('accounts:login')

        # Login direto
        login(request, user)
        try:
            colaborador = Colaboradores.objects.get(user=user)
            request.session['nome_colaborador'] = colaborador.nome_colaborador
        except Colaboradores.DoesNotExist:
            request.session['nome_colaborador'] = request.user.first_name or request.user.email
        return redirect('colaboradores:menu')    
    return render(request, 'app_login/pages/tela_login.html')

def esqueceu_senha(request):
    return render(request, 'app_login/pages/esqueceu_senha.html')

def logout(request):
    auth.logout(request)
    return redirect('accounts:login')