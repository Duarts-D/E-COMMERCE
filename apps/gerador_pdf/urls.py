from django.urls import path
from apps.gerador_pdf.views import gerador_html


app_name = 'gerar'

urlpatterns = [
    path('gerar_pdf/<int:pk>', gerador_html, name='gerar_pdf'),
]