from django.urls import path
from apps.produto.views import BuscarView,DetalheView,ProdutosView,ProdutosPromoView


app_name = 'produto'

urlpatterns = [
    path('',ProdutosView.as_view(),name='produtos'),
    path('<slug>',DetalheView.as_view(),name='detalhe'),
    path('buscar/',BuscarView.as_view(),name='buscar'),
    path('feitopravoce/',ProdutosPromoView.as_view(),name='promocoes'),
]