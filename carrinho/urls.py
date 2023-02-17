from django.urls import path
from carrinho.views import AdcCarrinho,Carrinho

app_name = 'cars'

urlpatterns = [
    path('',Carrinho.as_view(),name='carrinho'),
    path('adc_carrinho',AdcCarrinho.as_view(),name='adc_carrinho'),
]
