from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.menu, name='menu'),  # página inicial do menu
    path('cadastrar_colaborador/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('cadastrar_equipamento/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('visualizar_emprestimos/', views.visualizar_emprestimos, name='visualizar_emprestimos'),
    path('lista_colaborador/', views.lista_colaborador, name='lista_colaborador'),
    path('login/', views.login, name='login'),
    path('perfil/', views.perfil, name='perfil'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)