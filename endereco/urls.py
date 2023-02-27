from django.urls import path
from endereco.views import Endereco,EnderecoAlterar

app_name = 'enderecos'

urlpatterns = [
    path('',Endereco.as_view(),name='endereco'),
    path('atualizar/',EnderecoAlterar.as_view(),name='endereco_alterar')

]
