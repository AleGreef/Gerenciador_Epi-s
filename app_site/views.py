from django.shortcuts import render

def cadastrar_colaborador(request):
    return render(request, 'app_site/pages/cadastrar_colaborador.html')

def cadastrar_equipamento(request):
    return render(request, 'app_site/pages/cadastrar_equipamento.html')

def visualizar_emprestimos(request):
    return render(request, 'app_site/pages/visualizar_emprestimos.html')

def menu(request):
    return render(request, 'app_site/pages/menu.html')  # 'menu.html' é o template da tela do menu
