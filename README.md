
# LOJA - GAMERS E-ECOMMERCE
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/Duarts-D/E-COMMERCER/blob/master/LICENSE)

## Demonstração

http://loja-gamer.sa-east-1.elasticbeanstalk.com/

- login = lojagamerservidor@gmail.com
- senha = Username123

# Sobre o projeto


A loja Gamer - E estilo e-commerce criado com python, django, bootstrap e outros.

E uma loja de vendas funcional que agrega do início da compra até a hora do pagamento, sempre escolhendo a facilidade para melhorar a experiência do usuário.

Com sistema de cadastro, e-mails, recuperações de senha, local para verificação de pedido, também contem uma área para só promoções.

Utilizamos sessões para manter o controle dos nossos carrinhos de produtos.

Integrado também com sistema de gerador de PDF para funcionários manter organizado retirada de estoque,

Sempre focado na melhor experiência do usuário e otimizando as consultas no banco de dados.


# Layout web
- Pagina Inicial

 ![web 1](https://github.com/Duarts-D/E-COMMERCER/blob/master/img/pagina_incial_1.JPG)
 ![web 2](https://github.com/Duarts-D/E-COMMERCER/blob/master/img/pagina_incial_2.JPG)

- Produto
 <img src="https://github.com/Duarts-D/E-COMMERCER/blob/master/img/produto.JPG" alt="Produto" width="600" height="auto">

- Carrinho Compras
 <img src="https://github.com/Duarts-D/E-COMMERCER/blob/master/img/carrinho.JPG" alt="Carrinho Compras" width="600" height="auto">

- Resulmo da Compra
 <img src="https://github.com/Duarts-D/E-COMMERCER/blob/master/img/resulmo_compra.JPG" alt="Resulmo da compra" width="600" height="auto">

- Detalhe da Compra
 <img src="https://github.com/Duarts-D/E-COMMERCER/blob/master/img/detlhes_compra.JPG" alt="Detalhe compra" width="600" height="auto">

- Email
 <img src="https://github.com/Duarts-D/E-COMMERCER/blob/master/img/envio_email_compra.JPG" alt="E-mail" width="600" height="auto">

- PDF
<img src="https://github.com/Duarts-D/E-COMMERCER/blob/master/img/gerador_pdf_estoque.JPG" alt="PDF" width="600" height="auto">

# Tecnologias utilizadas


# black-end
- Python
- Django
- Bs4
- Pdfkit
- Pillow
- Python-decouple
- Python-dotenv
- Requests

# frond-end web
- HTML / CSS / JS 
- Bootstrap

# PDF
Para roda o gerador de PDF necessario  conter instalado na sua maquina
wkhtmltopdf 0.12.5 +

# E-mail
Para funcionadade e-mail , inserir dados em apps.config.py  e-mail 

## Como execultar o projeto

```bash
# clonar repositório
git clone https://github.com/Duarts-D/E-COMMERCER.git

# Versao Python 3.10.10
Para roda o programa sem ocorrer travamentos, necessario
python 3.10.10

# Criar ambiente virtual
Windows - python -m venv venv
linux - python3 -m venv venv

# Ativando ambiente virtual
Windows - .\venv\Scripts\Activate.ps1
linux - source ./venv/bin/activate

# instalar dependências
pip install -r requeriments.txt

# rodando migraçoes
windows - python manage.py makemigrations
windows - python manage.py migrate

linux - python3 manage.py makemigrations
linux - python3 manage.py migrate

# Popular banco de dados
linux - python3 insert_banco.py
windows - python insert_banco.py

# executar o projeto
windows - python manage.py runserver
linux - python3 manage.py runserver
```

## Se preferir Docker
```bash
# Executar Docker Compose 
''' Esta configurado para pre-popular banco de dados'''
Docker - docker compose up -d 

```
