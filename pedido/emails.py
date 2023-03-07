import base64
from django.shortcuts import render,redirect,reverse,get_object_or_404,get_list_or_404
from pedido.models import Pedido,Itempedido
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

def pedido_emailview(pk,email):
    pedido = get_object_or_404(Pedido,pk=pk)
    itempedido = get_list_or_404(Itempedido,pedido=pedido)
    imagem_codificadas = {}
    for imagem in itempedido:
        img_path = 'media/'+ imagem.imagem
        with open(img_path,'rb') as f:
            imagem_codificada = base64.b64encode(f.read()).decode("utf-8")
            imagem_codificadas[imagem.imagem] = imagem_codificada
    contexto={'imagens':imagem_codificadas,
              'produto':pedido,
              'itempedido':itempedido,
                }


    html_content = render_to_string('pedidos/emails/pedido_email.html',contexto)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
    'Compra realizada',
    text_content,
    settings.EMAIL_HOST_USER,
    [email]
    )

            
    email.attach_alternative(html_content,'text/html')
    for nome,imagem_codificada in imagem_codificadas.items():
        email.attach(nome,base64.b64decode(imagem_codificada),'image/jpg')       

    email.send()
    return redirect('pedido:lista')