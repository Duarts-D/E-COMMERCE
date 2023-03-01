from django.urls import path
from produto.views import ProdutosView,DetalheView,BuscarView
app_name = 'produto'

urlpatterns = [
    path('',ProdutosView.as_view(),name='produtos'),
    path('<slug>',DetalheView.as_view(),name='detalhe'),
    path('buscar/',BuscarView.as_view(),name='buscar')
]