from django.urls import path
from pedido.views import Pedido_PD,Salvar_pedido,ListPedido,Detalhe,pedido_emailview

app_name = 'pedido'

urlpatterns = [
    path('',Pedido_PD.as_view(),name='pedido'),
    path('salvar_pedido/',Salvar_pedido.as_view(),name='salvar_pedido'),
    path('lista/',ListPedido.as_view(),name='lista'),
    path('detalhe/<int:pk>',Detalhe.as_view(),name='detalhe'),


]
