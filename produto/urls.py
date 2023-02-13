from django.urls import path
from produto.views import Produtos,Detalhe

app_name = 'produto'

urlpatterns = [
    path('',Produtos.as_view(),name='produtos'),
    path('<slug>',Detalhe.as_view(),name='detalhe'),
    # path('produto/<int:id_url>',detalhe,name='detalhe')
]