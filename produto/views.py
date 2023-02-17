from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from produto.models import Produto
from django.core.paginator import Paginator

class Produtos(ListView):
    model = Produto
    template_name = 'produtos/produtos.html'
    context_object_name = 'produtos'
    paginate_by = 8
    ordering = ('id')
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(publico=True)
        return qs
        
class Detalhe(DetailView):
    model = Produto
    template_name = 'produtos/detalhe_produto.html'
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
