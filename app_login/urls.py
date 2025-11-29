from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login_view, name='login'),# página inicial 
    path('logout/', views.logout, name='logout'),
    path('criar_usuario/', views.criar_usuario, name='criar_usuario'),
    path('esqueceu_senha/', views.esqueceu_senha, name='esqueceu_senha'),
]
