from django.template import Library
register = Library()

@register.filter(name='sim_nao')
def qtdcarrinho(valor):
    if valor is True:
        return 'Sim'
    return 'Não'

