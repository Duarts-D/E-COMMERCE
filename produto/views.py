from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from produto.models import Produto
from django.core.paginator import Paginator
from django.db.models import Q,Value
from django.db.models.functions import Concat
import re

class ProdutosView(ListView):
    model = Produto
    template_name = 'produtos.html'
    context_object_name = 'produtos'
    paginate_by = 8
    ordering = ('id')
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(publico=True)
        return qs
        
class DetalheView(DetailView):
    model = Produto
    template_name = 'detalhe_produto.html'
    context_object_name = 'detalhe'
    slug_url_kwarg = 'slug'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        produto = self.get_object()
        produtos = Produto.objects.all().order_by('id').filter(publico=True,categoria=produto.categoria)

        paginator = Paginator(produtos, self.paginate_by )
        
        page = self.request.GET.get('page')
        
        page_obj = paginator.get_page(page)

        contexto['page_obj'] = page_obj

        
        return contexto

class BuscarView(ProdutosView):
    template_name = 'produtos.html'
    

    def get_queryset(self) :
        qs = super().get_queryset()
        busca = self.request.GET.get('buscar')
        info_busca = Concat('nome', Value(' '), 'categoria')
        if busca is None or not busca:
            return qs
        qs = qs.annotate(
            nome_categoria = info_busca
        ).filter(
            Q(nome_categoria__icontains=busca)|
            Q(nome__icontains=busca)|
            Q(descricao_longa__icontains=busca)|
            Q(slug__icontains=busca)
        )
        return qs

    def get(self,*args,**kwargs):
        get = super().get(*args,**kwargs)
        if not self.request.GET.get('buscar'):
            return redirect('produto:produtos')
        return get
    
class ProdutosPromoView(ListView):
    model = Produto
    template_name = 'produtos.html'
    context_object_name = 'produtos'
    paginate_by = 8
    ordering = ('id')
    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        qs = qs.filter(publico=True)
        qs = qs.exclude(preco_promocional=0)
        return qs
