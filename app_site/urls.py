from django.urls import path
from . import views

app_name = 'colaboradores'

urlpatterns = [
    path('menu/', views.menu, name='menu'),  
    path('cadastrar_colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('cadastrar_equipamento/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('cadastrar_setor/', views.cadastrar_setor, name='cadastrar_setor'),
    path('listar_emprestimos/', views.listar_emprestimos, name='listar_emprestimos'),
    path('listar_colaborador/', views.listar_colaborador, name='listar_colaborador'),
    path('listar_equipamentos/', views.listar_equipamentos, name='listar_equipamentos'),
    path('listar_setor/', views.listar_setor, name='listar_setor'),
    path('editar_colaborador/<int:id>', views.editar_colaborador, name='editar_colaborador'),
    path('editar_equipamento/<int:id>', views.editar_equipamento, name='editar_equipamento'),
    path('editar_setor/<int:id>', views.editar_setor, name='editar_setor'),
    path('remover_colaborador/<int:id>', views.remover_colaborador, name='remover_colaborador'),
    path('remover_equipamento/<int:id>', views.remover_equipamento, name='remover_equipamento'),
    path('remover_setor/<int:id>', views.remover_setor, name='remover_setor'),
    path('realizar_emprestimo/', views.realizar_emprestimo, name='realizar_emprestimo'),  
    path('perfil/', views.perfil, name='perfil'),
]

