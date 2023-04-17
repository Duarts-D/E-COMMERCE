from django.template import Library
from utilidade.ultils import qtdcar,valoresp,total_valoresp
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
