from django.urls import path
from usuario.views import Login,Cadastro,Logout,AtualizarDadosgr,AtualizarSenhaview,senha_sucesso,recuperar_senha_enviado,RecuperarSenhaView,RecuperarSenhaConfirmView
from django.contrib.auth import views as auth_views

app_name = 'usuario'

urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('cadastro/',Cadastro.as_view(),name='cadastro'),
    path('atualizar/',AtualizarDadosgr.as_view(),name='atualizardados_gr'),
    path('logout/',Logout.as_view(),name='logout'),
    
    path('atualizar_senha/',AtualizarSenhaview.as_view(template_name='usuarios/atualizar_senha.html'),name='atualizar_senha'),
    path('atualizacao_concluida/',senha_sucesso,name='atualizacao_concluida'),

    path('recuperar_senha/', RecuperarSenhaView.as_view(template_name = 'usuarios/resetar_senha/senha_reset_form.html'), name="reset_password"),
    path('recuperar_enviado/', recuperar_senha_enviado, name="recuperar_senha_enviado"),
    path('recuperar/<uidb64>/<token>', RecuperarSenhaConfirmView.as_view(template_name='usuarios/resetar_senha/senha_reset_confirma.html'), name="password_reset_confirm"),
    path('recuperar_bem_sucedido/', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/resetar_senha/senha_reset_completo.html'), name="password_reset_complete"),
 ]