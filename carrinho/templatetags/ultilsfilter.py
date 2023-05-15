from django.template import Library
from utilidade.ultils import qtdcar,valoresp,total_valoresp,valor_total_frete,email_valor_frete
register = Library()

@register.filter(name='qtdcar')
def qtdcarrinho(valor):
    return qtdcar(valor)

@register.filter(name='valores')
def valores(valor):
    return valoresp(valor)

@register.filter(name='total_valores')
def total_valor(total):
    return total_valoresp(total)

@register.filter(name='total_frete')
def valor_total_frt(carrinho,frete):
    return valor_total_frete(carrinho,frete)

@register.filter(name='email_frete')
def email_frete(valor_total,frete):
    return email_valor_frete(valor_total,frete)