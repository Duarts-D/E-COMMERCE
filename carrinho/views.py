from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from produto.models import Produto
from urllib.parse import urlparse
import re
from utilidade.frete_correio import CalcularFreteCarrinho
from usuario.models import Perfil_Usuario
from endereco.models import Perfil_Endereco
from utilidade.validators.cep import validador_cep

class AdcCarrinho(View):
    def get(self,*args,**kwargs):

        http_refere = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:produtos')
        )
        produto_ids = self.request.GET.get('car')
        
        
        if not produto_ids:
            messages.error(
                self.request,
                'Produto nao existe! ')
            return redirect(http_refere)
       
        if re.search(r'[^0-9]', produto_ids):
            messages.error(
                self.request,
                'Algo nao esta certo! ')
            return redirect(http_refere)            

        produto = get_object_or_404(Produto,id=produto_ids)
        produto_estoque = produto.estoque
        
        
        produto_nome = produto.nome
        preco_unitario = produto.preco 
        preco_unitario_promo = produto.preco_promocional
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''
        
        if produto_estoque <1:
            messages.info(self.request,'Estoque insuficiente')
            return redirect(http_refere)
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if produto_ids in carrinho:

            quantidade_carrinho = carrinho[produto_ids]['quantidade']
            quantidade_carrinho += 1


            if produto_estoque < quantidade_carrinho:
                messages.error(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no'
                    f'produto "{produto_nome}". Adicionamos {produto_estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = produto_estoque
            

            carrinho[produto_ids]['quantidade'] = quantidade_carrinho

            if carrinho[produto_ids]['quantidade'] >= 1  :
                carrinho[produto_ids]['preco_unitario'] = preco_unitario
                carrinho[produto_ids]['preco_unitario_promo'] = preco_unitario_promo
                carrinho[produto_ids]['preco_total_unitario'] = preco_unitario*\
                    quantidade_carrinho
                carrinho[produto_ids]['preco_total_promo'] = preco_unitario_promo*\
                    quantidade_carrinho

        else:
            carrinho[produto_ids] = {
            'produto_ids' : produto_ids,
            'produto_nome' : produto_nome,
            'preco_unitario' : preco_unitario,
            'preco_total_unitario' : preco_unitario,
            'preco_unitario_promo' : preco_unitario_promo,
            'preco_total_promo' : preco_unitario_promo,
            'quantidade' : 1,
            'slug' : slug,
            'imagem' : imagem,
            }
        self.request.session.save()
        
        messages.success(
            self.request,
            f'Produto {produto_nome} - Adicionado ao seu'
            f' Carrinho {carrinho[produto_ids]["quantidade"]}x. '
        )

        if 'HTTP_REFERER' in self.request.META:
            url_anterior = self.request.META['HTTP_REFERER']
            path_anterior = urlparse(url_anterior).path
            pach_slug = f'/{slug}'
            if path_anterior is '/':
                return redirect('cars:carrinho')
            if path_anterior == pach_slug:
                return redirect('cars:carrinho')

        return redirect(http_refere)

class Carrinho(View):
    template_name = 'carrinho.html'
    contexto = {}
    
    def post(self,*args,**kwargs):
        cep = self.request.POST.get('CEP')

        if not validador_cep(cep):
            messages.error(self.request,f'Cep invalido {cep}')
            return redirect('cars:carrinho')
        
        endereco = validador_cep(cep)

        carrinho = self.request.session.get('carrinho')
        frete = CalcularFreteCarrinho(carrinho=carrinho,cep_destino=cep)
        frete = frete.calcular_frete_carrinho()
        self.contexto = {
            'frete_entrega': frete[0],
            'preco': frete[1],
            'carrinho' : self.request.session.get('carrinho',{}),
            'endereco': endereco
        }

        return render(self.request,self.template_name,self.contexto)

    def get(self,*args,**kwargs):
        
        if self.request.user.is_authenticated:
            perfil = Perfil_Usuario.objects.get(user=self.request.user)
            cep = Perfil_Endereco.objects.get(user_perfil=perfil).cep

            if self.request.session.get('carrinho'):
                carrinho = self.request.session.get('carrinho')
                frete = CalcularFreteCarrinho(carrinho=carrinho,cep_destino=cep)
                frete = frete.calcular_frete_carrinho()
                self.contexto = {
                    'frete_entrega': frete[0],
                    'preco': frete[1],
                }
        self.contexto['carrinho'] = self.request.session.get('carrinho',{})
        

        return render(self.request,self.template_name,self.contexto)

class DelCarrinho(View):
    def get(self,*args,**kwargs):
                
        http_refere = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:produtos')
            )
        produto_id = self.request.GET.get('car_del')

        
        if not produto_id:
            return redirect(http_refere)
        
        if not produto_id in self.request.session['carrinho']:
            return redirect(http_refere)

        if not self.request.session['carrinho']:
            return redirect(http_refere)
            
        del_carrinho = self.request.session['carrinho'][produto_id]
        messages.success(
            self.request,
            f'{del_carrinho["produto_nome"]}'
            f' removido do seu carrinho')
        
        del self.request.session['carrinho'][produto_id]
        self.request.session.save()
        
        return redirect(http_refere)
        
class DelCarrinho_Unitario(View):
    def get(self,*args,**kwargs):
        http_refere = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:produtos')
            )
        produto_id = self.request.GET.get('car_del')


        if not produto_id:
            return redirect(http_refere)
        
        carrinho = self.request.session['carrinho']
        

        if not produto_id in carrinho[produto_id]['produto_ids']:
            return redirect('produto:produtos')

        quantidade_carrinho = carrinho[produto_id]['quantidade']
        quantidade_carrinho -= 1

        if quantidade_carrinho <= 0:
            return redirect(http_refere)
        
        preco_unitario = carrinho[produto_id]['preco_unitario']
        preco_promo = carrinho[produto_id]['preco_unitario_promo']

        carrinho[produto_id]['quantidade'] = quantidade_carrinho
        
        if carrinho[produto_id]['quantidade'] >= 1:
            carrinho[produto_id]['preco_total_unitario'] = preco_unitario*\
                quantidade_carrinho
            carrinho[produto_id]['preco_total_promo'] = preco_promo*\
                quantidade_carrinho
        else:
            carrinho[produto_id]['preco_total_unitario'] = 0
            carrinho[produto_id]['preco_total_promo'] = 0
            
        messages.warning(self.request,f'{carrinho[produto_id]["produto_nome"]}'
            f' Retirado do seu carrinho.')
        self.request.session.save()
        return redirect(http_refere)

        
        