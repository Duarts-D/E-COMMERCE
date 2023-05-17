def qtdcar(carrinho):
        return sum([item['quantidade'] for item in carrinho.values()])

def valoresp(valor):
        if not valor is None or '':
                valores = f'R${valor:_.2f}'.replace('.',',').replace('_','.')
                return valores
        return f'Valor incorreto'

def total_valoresp(valores):
        valor_total = sum(
                [
                        item.get('preco_total_promo') 
                        if item.get('preco_total_promo')
                        else 
                        item.get('preco_total_unitario')
                        for item in valores.values()
                ])
        vlaor = round(valor_total,2)
        return vlaor

def valor_total_frete(carrinho,frete):
        if frete is True:
                return valoresp(total_valoresp(carrinho))
        else:
                frete = str(frete).replace('R$','').replace(',','.')
                frete = float(frete)
                valor_total_carrinho = total_valoresp(carrinho)
                total = frete + valor_total_carrinho        
                total = valoresp(total)
                return total

def email_valor_frete(valor_total,frete):
        frete = float(str(frete).replace(',','.'))
        valor_total = float(str(valor_total).replace(',','.'))
        total = valor_total + frete
        return total