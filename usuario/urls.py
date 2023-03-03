from django.urls import path
from usuario.views import Login,Cadastro,Logout,AtualizarDadosgr,AtualizarSenhaview,senha_sucesso
from django.contrib.auth import views as auth_views

app_name = 'usuario'

urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('cadastro/',Cadastro.as_view(),name='cadastro'),
    path('atualizar/',AtualizarDadosgr.as_view(),name='atualizardados_gr'),
    path('logout/',Logout.as_view(),name='logout'),
    
    path('atualizar_senha/',AtualizarSenhaview.as_view(template_name='usuarios/atualizar_senha.html'),name='atualizar_senha'),
    path('atualizacao_concluida/',senha_sucesso,name='atualizacao_concluida'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='usuarios/resetar_senha/senha_reset_form.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/resetar_senha/senha_reset_enviada'), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
 ]