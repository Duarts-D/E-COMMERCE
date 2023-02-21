from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from produto.models import Produto
import re

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
        quantidade = 1
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
        return redirect('cars:carrinho')

class Carrinho(View):
    template_name = 'carrinho/carrinho.html'
    def get(self,*args,**kwargs):
        contexto = {
            'carrinho' : self.request.session.get('carrinho',{})
        }
        return render(self.request,self.template_name,contexto)

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
            f'Produto {del_carrinho["produto_nome"]}'
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
        
        if not produto_id in carrinho[produto_id]:
            return redirect('produto:produtos')

        quantidade_carrinho = carrinho[produto_id]['quantidade']
        quantidade_carrinho -= 1

        if quantidade_carrinho <= 0:
            return redirect(http_refere)
        
        preco_unitario = carrinho[produto_id]['preco_unitario']
        preco_promo = carrinho[produto_id]['preco_unitario_promo']

        carrinho[produto_id]['quantidade'] = quantidade_carrinho
        carrinho[produto_id]['preco_total_unitario'] = preco_unitario*\
            quantidade_carrinho
        carrinho[produto_id]['preco_total_promo'] = preco_promo*\
            quantidade_carrinho


        self.request.session.save()
        return redirect(http_refere)

        
        