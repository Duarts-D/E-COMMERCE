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
        produto_id = self.request.GET.get('car')
        
        
        if not produto_id:
            messages.error(
                self.request,
                'Produto nao existe! ')
            return redirect(http_refere)
       
        if re.search(r'[^0-9]', produto_id):
            messages.error(
                self.request,
                'Algo nao esta certo! ')
            return redirect(http_refere)            

        produto = get_object_or_404(Produto,id=produto_id)
        produto_estoque = produto.estoque
        
        produto_id = produto.id
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
        if produto_id in carrinho:
            quantidade_carrinho = carrinho[produto_id]['quantidade']
            quantidade_carrinho += 1

            if produto_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no'
                    f'produto "{produto_nome}". Adicionamos {produto_estoque}x'
                    f'no seu carrinho.'
                )
                quantidade_carrinho = produto_estoque
            
            carrinho[produto_id]['quantidade'] = quantidade_carrinho
            carrinho[produto_id]['preco_total_unitario'] = preco_unitario*\
                quantidade_carrinho
            carrinho[produto_id]['preco_total_promo'] = preco_unitario_promo*\
                quantidade_carrinho
        else:
            carrinho[produto_id] = {
            'produto_id' : produto_id,
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
                f'Carrinho {carrinho[produto_id]["quantidade"]}x. '
            )
        return redirect('cars:carrinho')

class Carrinho(View):
    template_name = 'carrinho/carrinho.html'
    def get(self,*args,**kwargs):
        contexto = {
            'carrinho' : self.request.session.get('carrinho',{})
        }
        return render(self.request,self.template_name,contexto)