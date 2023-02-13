from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from produto.models import Produto

class Produtos(ListView):
    model = Produto
    template_name = 'produtos/produtos.html'
    context_object_name = 'produtos'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(publico=True)
        return qs
        
class Detalhe(DetailView):
    model = Produto
    template_name = 'produtos/detalhe_produto.html'
    context_object_name = 'detalhe'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        produto = self.get_object()
        produtos = Produto.objects.filter(publico=True,categoria=produto.categoria)
        contexto['produtos'] = produtos
        
        return contexto
