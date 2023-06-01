import json
import sqlite3
import shutil
import os


def pre_imagens():
    '''Adiciona as imagens para ser utilizada com ó pre banco de dados'''
    
    caminho = 'img/pre_imagens'
    media = 'media'
    media_pre = 'media/pre_imagens'
    
    try:
        os.mkdir(media)
        os.mkdir(media_pre)
    except FileExistsError as e:
        print(f'Pasta ja criada')
        return True

    for root,dirs,names in os.walk(caminho):
        for name in names:
            caminho_origin = os.path.join(root,name)
            caminho_novo = os.path.join(media_pre,name)
            shutil.copy(caminho_origin,caminho_novo)
    return True

def sql_conexao():
    '''Popula inicialmente o banco de dados, se estiver vazio para primeira impressoes'''
    if pre_imagens() is True:
        conexao = sqlite3.connect('db.sqlite3')
        cursor = conexao.cursor()

        with open('produtos_dados.json',encoding='utf-8',) as dados:
            json_produtos = json.load(dados)
            
            try:
                coluna = cursor.execute("SELECT * FROM produto_produto")
            except :
                coluna = False
            
            if coluna is False:
                conexao.close()
                raise KeyError('OperationalErro - Favor fazer as migraçoes')

            for dados in json_produtos:
                ids = dados['id']
                nome = dados['nome']
                preco = dados['preco']
                preco_promocional = dados['preco_promocional']
                descricao_longa = dados['descricao_longa']
                estoque = dados['estoque']
                imagem = dados['imagem']
                publico = dados['publico']
                slug = dados['slug']
                categoria = dados['categoria']
                peso = dados['peso']
                comprimento =dados['comprimento']
                altura = dados['altura']
                largura = dados['largura']
                
                insercao_banco =f"""INSERT INTO produto_produto VALUES (
                    '{ids}','{nome}','{preco}','{preco_promocional}','{descricao_longa}',
                    '{estoque}','{publico}','{slug}','{categoria}','{imagem}','{altura}',
                    '{comprimento}','{largura}','{peso}')
                """

                try:
                    cursor.execute(insercao_banco)
                    conexao.commit()
                except:
                    print(f'Seu banco de dados ja esta populado')
                    break
        conexao.close()

if __name__ == "__main__":
    sql_conexao()