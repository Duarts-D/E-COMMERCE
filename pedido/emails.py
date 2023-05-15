from django.shortcuts import redirect,get_object_or_404,get_list_or_404
from pedido.models import Pedido,Itempedido
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from config import EMAIL_HOST_USER


def pedido_email_html(pk,email_user):
    pedido = get_object_or_404(Pedido,pk=pk)
    itempedido = get_list_or_404(Itempedido,pedido=pedido)

    imagens=[]
    for imagem in itempedido:
        img_path = 'media/'+ imagem.imagem
        with open(img_path,'rb') as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID',f'<{imagem.imagem}>')
        imagens.append(logo)

    contexto={'produto':pedido,
              'itempedido':itempedido,
                }
    
    html_content = (
        render_to_string('emails/pedido_email.html',contexto)
    )
    html_content_alt = (
                render_to_string('emails/pedido_email_anexos.html',contexto))
    
    email = EmailMultiAlternatives(
    'Compra realizada',
    html_content,
    EMAIL_HOST_USER,
    [email_user,]
    )

    email.attach_alternative(html_content_alt,'text/html')

    for anexo in imagens:
       email.attach(anexo)
    
    return email.send()