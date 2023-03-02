import re

def caract_especiais_validador(valor):
    return re.search(r'[^a-zA-Z0-9\s]', valor)

def string_validador(valor):
    return any( x.isdigit() for x in valor)

def tamanho_len_validador(valor,digito):
    return len(valor)<digito

def espaços_vazio_validador(valor):
    return ' ' in valor

def digitos_validador(valor):
    return re.search(r'[^0-9\s]', valor)