from django.contrib import admin
from pedido.models import Pedido,Itempedido
# Register your models here.

class ItemPedidoInline(admin.TabularInline):
    model = Itempedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]
admin.site.register(Pedido,PedidoAdmin)