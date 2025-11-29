from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.menu, name='menu'), # página inicial do menu
    path('gerenciar_colaboradores/', views.gerenciar_colaboradores, name='gerenciar_colaboradores'),
    path('cadastrar_colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('verificar_cpf/', views.verificar_cpf, name='verificar_cpf'),
    path('cadastrar_equipamento/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('visualizar_emprestimos/', views.visualizar_emprestimos, name='visualizar_emprestimos'),
    path('lista_colaborador/', views.lista_colaborador, name='lista_colaborador'),
    path('login/', views.login, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('excluir_colaborador/', views.excluir_colaborador, name='excluir_colaborador'),
    path('editar_colaborador/<str:cpf>/', views.editar_colaborador, name='editar_colaborador'),
    path('excluir_colaborador/', views.excluir_colaborador, name='excluir_colaborador'),
    path("realizar_reserva/", views.realizar_reserva, name="realizar_reserva"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)