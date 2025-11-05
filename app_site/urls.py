from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),  # página inicial do menu
    path('cadastrar_colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('cadastrar_equipamento/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('visualizar_emprestimos/', views.visualizar_emprestimos, name='visualizar_emprestimos'),
    path('listar_colaborador/', views.listar_colaborador, name='listar_colaborador'),
    path('listar_equipamentos/', views.listar_equipamentos, name='listar_equipamentos'),
    path('login/', views.login, name='login'),
]
