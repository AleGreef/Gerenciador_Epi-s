from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'), # página inicial do menu
    path('gerenciar_col/', views.gerenciar_colaboradores, name='gerenciar_colaboradores'),
    path('cadastrar_colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('verificar_cpf/', views.verificar_cpf, name='verificar_cpf'),
    path('cadastrar_equipamento/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('visualizar_emprestimos/', views.visualizar_emprestimos, name='visualizar_emprestimos'),
    path('lista_colaborador/', views.lista_colaborador, name='lista_colaborador'),
]
