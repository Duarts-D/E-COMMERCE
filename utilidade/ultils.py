def qtdcar(carrinho):
        return sum([item['quantidade'] for item in carrinho.values()])