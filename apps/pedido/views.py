from django.contrib import messages
from django.shortcuts import render,redirect,reverse,get_list_or_404
from django.views import View
from django.views.generic import DetailView,ListView
from apps.endereco.models import Perfil_Endereco
from apps.usuario.models import Perfil_Usuario
from apps.utilidade.ultils import qtdcar,total_valoresp
from apps.pedido.models import Pedido,Itempedido
from apps.pedido.emails import pedido_email_html
from apps.produto.models import Produto


class Pedido_PD(View):
    template_name ='pedido.html'
    
    def setup(self,request,*args,**kwargs):
        super().setup(request,*args,**kwargs)

        self.user_on = self.request.user.is_authenticated

        if not self.user_on:
            return redirect('usuario:login')
        user = Perfil_Usuario.objects.filter(user=self.request.user).first()
        
        perfil_user = Perfil_Endereco.objects.get(user_perfil=user.id)
        
        frete = self.request.session.get('frete')
        self.contexto = {
            'perfil_usuario': perfil_user, 
            'carrinho': self.request.session.get('carrinho'),
            'preco':frete['preco']
        }

    def get(self,*args,**kwargs):
        if not self.user_on:
            return redirect('usuario:login')

        user = Perfil_Usuario.objects.filter(user=self.request.user).first()
        perfil_user = Perfil_Endereco.objects.filter(user_perfil=user.id).exists()

        if user is None or perfil_user is None :
            return redirect('usuario:login')
        
        return render(self.request,self.template_name,self.contexto)

class Salvar_pedido(View):
    template_name = 'pedido.html'

    def get(self,*args,**kwargs):

        if not self.request.user.is_authenticated:
            return redirect('usuario:login')
        
        if not self.request.session.get('carrinho'):
            return redirect('cars:carrinho')
        
        carrinho = self.request.session.get('carrinho')

        carrinho_produtos_ids = [ c for c in carrinho]
        bd_produtos_ids = Produto.objects.filter(id__in=carrinho_produtos_ids)

        for produto in bd_produtos_ids:
            vid = str(produto.id)

            estoque = produto.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unit = carrinho[vid]['preco_unitario_promo']
            preco_unit_promo = carrinho[vid]['preco_unitario_promo']
            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_unitario'] = estoque * preco_unit
                carrinho[vid]['preco_unitario_promo'] = estoque*\
                    preco_unit_promo
                carrinho[vid]['preco_total_unitario'] = estoque*\
                    preco_unit_promo
                carrinho[vid]['preco_total_promo'] = estoque*\
                    preco_unit_promo

                error_msg_estoque ='Estoque insuficiente para alguns produtos do seu carrinho.'\
                'Reduzimos a quantidade desse produtos. Por favor, verifique'\
                'quais produtos foram afetados a seguir.'\

                if error_msg_estoque:
                    messages.error(self.request,error_msg_estoque)
                    
                self.request.session.save()
                return redirect('cars:carrinho')
            
        for produto in bd_produtos_ids:
            vid = str(produto.id)
            if carrinho[vid]["quantidade"] == 0 :
                del carrinho[vid]
                
        qtd_total_carrinho = qtdcar(carrinho)
        valor_total_carrinho = total_valoresp(carrinho)

        frete = self.request.session.get('frete')
        pedido = Pedido(
            user=self.request.user,
            total= qtd_total_carrinho,
            qtd_valor_total= valor_total_carrinho,
            status = 'P',
            frete = frete['preco']
        )

        pedido.save()
        
        Itempedido.objects.bulk_create(
             [Itempedido(
                pedido=pedido,
                produto=v['produto_nome'],
                produto_id=v['produto_ids'],
                preco_unitario=v['preco_unitario'],
                preco_total_unitario=v['preco_total_unitario'],
                preco_unitario_promo=v['preco_unitario_promo'],
                preco_total_promo=v['preco_total_promo'],
                quantidade=v['quantidade'],
                imagem=v['imagem'],
                slug=v['slug']
            ) for v in carrinho.values()
            ]
         )
        del self.request.session['carrinho']

        qtd_produto = get_list_or_404(Itempedido,pedido=pedido.pk)
        
        for produto in qtd_produto:
            produto_id  = Produto.objects.get(id=produto.produto_id)
            estoque = produto_id.estoque 
            produto_id.estoque = estoque - produto.quantidade
            produto_id.save()
        
        pedido_email_html(pk=pedido.pk,email_user=self.request.user.email,valor_frete=frete)
        messages.success(self.request,'Compra Realizada com Sucesso')
        
        return redirect(reverse('pedido:detalhe',kwargs={'pk':pedido.pk}))

class ListPedido(ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'status_pedido.html'
    paginate_by = 4
    ordering = ['-id']
    
    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        qs = qs.filter(user=self.request.user)
        return qs
    
    def get(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            return redirect('usuario:login')
        return super().get(*args,**kwargs)
    
class Detalhe(DetailView):
    model = Pedido
    context_object_name = 'produto'
    template_name = 'detalhe_pedido.html'
    pk_url_kwarg = 'pk'
    
    def get(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            return redirect('usuario:login')
        return super().get(*args,**kwargs)

class OsServicosView(ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'status_pedido.html'
    paginate_by = 10 
    ordering = ['-pk']