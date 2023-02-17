from django.template import Library
from utilidade.ultils import qtdcar
register = Library()

@register.filter(name='qtdcar')
def qtdcarrinho(valor):
    return qtdcar(valor)