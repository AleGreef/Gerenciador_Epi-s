from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),  # página inicial vai para o login
    path('logout_view/', views.logout_view, name='logout_view'),
    path('esqueceu_senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('cadastrar_colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastrar_setor/', views.cadastrar_setor, name='cadastrar_setor'),
    path('cadastrar_equipamento/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('visualizar_emprestimos/', views.visualizar_emprestimos, name='visualizar_emprestimos'),
    path('listar_colaborador/', views.listar_colaborador, name='listar_colaborador'),
    path('listar_equipamentos/', views.listar_equipamentos, name='listar_equipamentos'),
    path('listar_setores/', views.listar_setores, name='listar_setores'),
    path('realizar_emprestimos/', views.realizar_emprestimos, name='realizar_emprestimos'),
    path('menu/', views.menu, name='menu'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)