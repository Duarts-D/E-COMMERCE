from django.urls import path
from apps.usuario.views import (LoginView,CadastroView,Logout,
                           AtualizarDadosgrView,AtualizarSenhaview,
                           senha_sucesso,recuperarsenha_enviado,
                           recuperarsenhaconfirm_completo,
                           RecuperarSenhaView,RecuperarSenhaConfirmView)


app_name = 'usuario'

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('cadastro/',CadastroView.as_view(),name='cadastro'),
    path('logout/',Logout.as_view(),name='logout'),

    path('atualizar/',AtualizarDadosgrView.as_view(),name='atualizardados_gr'),
    path('atualizar_senha/',AtualizarSenhaview.as_view(),name='atualizar_senha'),
    path('atualizacao_concluida/',senha_sucesso,name='atualizacao_concluida'),

    path('recuperar_senha/', RecuperarSenhaView.as_view(), name="reset_password"),
    path('recuperar_enviado/', recuperarsenha_enviado, name="recuperar_senha_enviado"),
    path('recuperar/<uidb64>/<token>', RecuperarSenhaConfirmView.as_view(), name="password_reset_confirm"),
    path('recuperar_bem_sucedido/', recuperarsenhaconfirm_completo,name="password_reset_complete"),
 ]