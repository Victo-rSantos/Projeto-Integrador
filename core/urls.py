from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                     # Página inicial
    path('cadastro/', views.cadastro_view, name='cadastro'),  # Cadastro de usuário
    path('guest/', views.guest_view, name='guest'),           # Entrar como visitante
    path('sala/', views.sala_view, name='sala'),              # Sala de aula (única página principal)
    path('deletar/<int:id>/', views.deletar_comentario, name='deletar_comentario'),  # Professores deletam mensagens
    
]
