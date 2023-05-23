from django.urls import path
from apps.carrinho.views import AdcCarrinho,Carrinho,DelCarrinho,DelCarrinho_Unitario


app_name = 'cars'

urlpatterns = [
    path('',Carrinho.as_view(),name='carrinho'),
    path('adc_carrinho',AdcCarrinho.as_view(),name='adc_carrinho'),
    path('del_carrinho/',DelCarrinho.as_view(),name='del_carrinho'),
    path('del_carrinho_unitario/',DelCarrinho_Unitario.as_view(),name='del_carrinho_unitario'),
]
