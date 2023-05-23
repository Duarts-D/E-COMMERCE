from django.contrib import admin
from apps.pedido.models import Pedido,Itempedido


class ItemPedidoInline(admin.TabularInline):
    model = Itempedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]
    
admin.site.register(Pedido,PedidoAdmin)