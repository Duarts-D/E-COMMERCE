import requests

def validador_cep(cep):
    if len(cep) != 8 or not cep.isdigit():
        return False

    api_cep = f'https://viacep.com.br/ws/{cep}/json/'
    dados = requests.get(api_cep).json()

    if 'erro' in dados:
        return False
    else:
        endereco = {
            'rua_avenida' : dados['logradouro'],
            'bairro' : dados['bairro'],
            'localidade' : dados['localidade'],
            'uf' : dados['uf']
        }
    return endereco