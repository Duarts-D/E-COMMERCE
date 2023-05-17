from utilidade.ultils import total_valoresp
from produto.models import Produto
from datetime import date
from bs4 import BeautifulSoup
import requests
from config import CEPORIGEM


class CalcularFreteCarrinho():
        def __init__(self,carrinho,cep_destino):
            self.carrinho = carrinho
            self.cep_destino = cep_destino
            self.produtos = []

            self.p_altura = 0
            self.p_largura = 0
            self.p_comprimento = 0
            self.p_peso = 0
        
        def desconto(self,valor):
            total = total_valoresp(self.carrinho)
            tempo_de_entrega , valores = valor
            if total >= 3000 and float(valores) <= 200:
                preco = True
                return tempo_de_entrega, preco
            return valor
            
        def produto_alt_comp(self):
            for produto_id in self.carrinho:
                produto_query = Produto.objects.get(id=produto_id)
                if self.p_altura <= produto_query.altura:
                    self.p_altura = produto_query.altura
                if self.p_comprimento <= produto_query.comprimento:
                    self.p_comprimento = produto_query.comprimento
                self.produtos.append(produto_query)
            
            return self.produtos

        def calcular_frete_carrinho(self):
            self.produto_alt_comp()
            
            for produto in self.produtos:
                quantidade = self.carrinho[str(produto.id)]['quantidade']
                
                if self.p_altura >= produto.altura * 2:
                    self.p_largura = produto.largura + self.p_largura
                else:
                    self.p_largura = (produto.largura * quantidade) + self.p_largura

                self.p_peso = (produto.peso * quantidade) + self.p_peso
            
            
            correio = CorreioWebscript(ceporigem=CEPORIGEM,
                                        cepdestino=self.cep_destino,
                                        altura=self.p_altura,
                                        largura=self.p_largura,
                                        comprimento=self.p_comprimento,
                                        peso=self.p_peso)
            valor = correio.frete()
            return self.desconto(valor)

class CorreioWebscript:
    def __init__(self,ceporigem,cepdestino,altura,largura,comprimento,peso):
        self.altura = altura
        self.ceporigim = ceporigem
        self.cepdestino = cepdestino
        self.comprimento = comprimento
        self.largura = largura
        self.peso = peso
        self.data = date.today().strftime('%d/%m/%Y')
  
    
    def dados(self):
        dados = {
            'data': self.data,
            'dataAtual': self.data,
            'cepOrigem': self.ceporigim,
            'cepDestino': self.cepdestino,
            'servico': '04510',
            'Calcular': 'Calcular',
            'Formato': '1',
            'embalagem1': 'outraEmbalagem1',
            'peso': self.peso,
            'Altura': self.altura,
            'Largura': self.largura,
            'Comprimento': self.comprimento,
            'Selecao': '',
            'embalagem2': '',
            'Selecao1': '',
            'proCod_in_1':'',
            'nomeEmbalagemCaixa': '',
            'TipoEmbalagem1': '',
            'Selecao2': '',
            'proCod_in_2': '',
            'TipoEmbalagem2': '',
            'Selecao3': '',
            'proCod_in_3': '',
            'TipoEmbalagem3': '',
            'Selecao4': '',
            'proCod_in_4': '',
            'TipoEmbalagem4': '',
            'Selecao5': '',
            'proCod_in_5': '',
            'TipoEmbalagem5': '',
            'Selecao6': '',
            'proCod_in_6': '',
            'TipoEmbalagem6': '',
            'Selecao7': '',
            'proCod_in_7': '',
            'TipoEmbalagem7': '',
            'Selecao14': '',
            'proCod_in_14': '',
            'TipoEmbalagem14': '',
            'Selecao15': '',
            'proCod_in_15': '',
            'TipoEmbalagem15': '',
            'Selecao16': '',
            'proCod_in_16': '',
            'TipoEmbalagem16': '',
            'Selecao17': '',
            'proCod_in_17': '',
            'TipoEmbalagem17': '',
            'Selecao18': '',
            'proCod_in_18': '',
            'TipoEmbalagem18': '',
            'Selecao19': '',
            'proCod_in_19': '',
            'TipoEmbalagem19': '',
            'Selecao20': '',
            'proCod_in_20': '',
            'Selecao8': '',
            'proCod_in_8': '',
            'nomeEmbalagemEnvelope': '',
            'TipoEmbalagem8': '',
            'Selecao9': '',
            'proCod_in_9': '',
            'TipoEmbalagem9': '',
            'Selecao10': '',
            'proCod_in_10': '',
            'Selecao11': '',
            'proCod_in_11': '',
            'Selecao12': '',
            'proCod_in_12': '',
            'TipoEmbalagem12': '',
            'Selecao13': '',
            'proCod_in_13': '',
            'TipoEmbalagem13': '',
            'Selecao21': '',
            'proCod_in_21': '',
            'TipoEmbalagem21': '',
            'Selecao22': '',
            'proCod_in_22': '',
            'TipoEmbalagem22': '',
            'Selecao23': '',
            'proCod_in_23':'', 
            'TipoEmbalagem23':'', 
            'Selecao24': '',
            'proCod_in_24':'', 
            'TipoEmbalagem24':'', 
            'Selecao25': '',
            'proCod_in_25':'', 
            'TipoEmbalagem25':'', 
            'Selecao26': '',
            'proCod_in_26':'', 
            'Selecao27': '',
            'proCod_in_27':'', 
            'Selecao28': '',
            'proCod_in_28':'', 
            'TipoEmbalagem28':'',
            'Selecao29': '',
            'proCod_in_29':'',
            'TipoEmbalagem29':'',
            'Selecao30':'',
            'proCod_in_30':'',
            'TipoEmbalagem30':'',
            'valorDeclarado':'',
        }
        return dados
    
    def frete(self):
        """Utilizando para fins didáticos raspagem do site https://www2.correios.com.br/sistemas/precosPrazos/, 
            Sem obtenção de lucro nenhum"""
        cabecalho ={'user-agent':'Mozilla/5.0'}
        url_correio_brasil = 'https://www2.correios.com.br/sistemas/precosPrazos/prazos.cfm' #

        resposta = requests.post(url_correio_brasil,headers=cabecalho,data=self.dados())
        html_respota = resposta.text

        html_bs4 = BeautifulSoup(html_respota,'html.parser')
        
        # Pegando preço frete
        preco = html_bs4.find_all('tfoot')
        preco = preco[0].find('td').text
        preco = preco.replace('R$','').replace(',','.').strip()
        preco = float(preco)

        # Pegando tempo de entrega 
        tempo_de_entrega = html_bs4.find_all('tbody')
        tempo_de_entrega = tempo_de_entrega[0].find_all('td')
        tempo_de_entrega = (tempo_de_entrega[2].text).replace('Dia da Postagem','Entrega apos o comfirmamento da compra')

        return tempo_de_entrega,preco
