from django.urls import path
from pedido.views import Pagamento

app_name = 'pedido'

urlpatterns = [
    path('',Pagamento.as_view(),name='pagamento')
]
