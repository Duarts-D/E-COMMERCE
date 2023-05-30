import os
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
import pdfkit
from rolepermissions.decorators import has_permission_decorator
from apps.pedido.models import Pedido

@has_permission_decorator('gerar_pdf')
def gerador_html(request,pk):
    pedido = Pedido.objects.get(pk=pk)
    path = os.path.join(settings.BASE_DIR)

    template = get_template('formulario_retirada_estoque.html')
    html = template.render({'pedido':pedido,'path':path})

    css = 'setup/static/css/styles.css'
    options = {
        'enable-local-file-access' : None,
        'page-size': 'A4',
        'encoding': 'UTF-8',
    }
    pdf = pdfkit.from_string(html,False,css=css,options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="arquivo.pdf'
    return response