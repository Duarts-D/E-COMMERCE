from django.urls import path
from usuario.views import Login,Cadastro,Logout,AtualizarDadosgr

app_name = 'usuario'

urlpatterns = [
    path('login',Login.as_view(),name='login'),
    path('cadastro',Cadastro.as_view(),name='cadastro'),
    path('atualizar',AtualizarDadosgr.as_view(),name='atualizardados_gr'),
    path('logout',Logout.as_view(),name='logout'),

 ]