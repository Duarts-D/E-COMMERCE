from django.urls import path
from usuario.views import Login,Cadastro,Logout

app_name = 'usuario'

urlpatterns = [
    path('login',Login.as_view(),name='login'),
    path('cadastro',Cadastro.as_view(),name='cadastro'),
    path('logout',Logout.as_view(),name='logout'),

 ]