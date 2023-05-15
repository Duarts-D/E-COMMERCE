import base64
from django.shortcuts import render,redirect,reverse,get_object_or_404,get_list_or_404
from pedido.models import Pedido,Itempedido
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from email.mime.image import MIMEImage

def pedido_emailview(pk,email):
    pedido = get_object_or_404(Pedido,pk=pk)
    itempedido = get_list_or_404(Itempedido,pedido=pedido)

    img=[]
    for imagem in itempedido:
        img_path = 'media/'+ imagem.imagem
        with open(img_path,'rb') as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID',f'<{imagem.imagem}>')
        img.append(logo)

    contexto={'produto':pedido,
              'itempedido':itempedido,
                }
    

    html_content = (
        render_to_string('emails/teste2.html',contexto)
    )
    html_content_alt = (
                render_to_string('emails/pedido_email.html',contexto))
    
    email = EmailMultiAlternatives(
    'Compra realizada',
    html_content,
    settings.EMAIL_HOST_USER,
    ['deividnaruto@hotmail.com','dddduartegtgt@gmail.com']
    )

            
    email.attach_alternative(html_content_alt,'text/html')


    for i in img:
       email.attach(i)
       
    email.send()
    return redirect('pedido:pedido')