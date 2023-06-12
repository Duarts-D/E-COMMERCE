from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404,get_list_or_404
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
try:
    decouple_config = True
    from apps.config import EMAIL_HOST_USER
except ImportError:
    decouple_config = False
from apps.pedido.models import Pedido,Itempedido


def pedido_email_html(pk,email_user,valor_frete):

    if decouple_config is False:
        return 'Config-email nao configurado'
    
    pedido = get_object_or_404(Pedido,pk=pk)
    itempedido = get_list_or_404(Itempedido,pedido=pedido)
    

    # Utilizar para  modo local arquivos acoplados no projeto
    # imagens=[]
    # for imagem in itempedido:
    #     img_path = 'media/' + imagem.imagem
    #     with open(img_path,'rb') as f:
    #         logo_data = f.read()
    #     logo = MIMEImage(logo_data)
    #     logo.add_header('Content-ID',f'<{imagem.imagem}>')
    #     imagens.append(logo)

    contexto={'produto':pedido,
                'itempedido':itempedido,
                'preco':valor_frete['preco']
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

    # for anexo in imagens:
      #  email.attach(anexo)
    
    return email.send()