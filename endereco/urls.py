from django.urls import path
from endereco.views import Endereco

app_name = 'enderecos'

urlpatterns = [
    path('',Endereco.as_view(),name='endereco')
]
