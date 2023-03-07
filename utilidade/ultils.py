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