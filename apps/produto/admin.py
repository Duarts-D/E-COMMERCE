from django.contrib import admin
from apps.produto.models import Modelo,Produto


class ModelosInline(admin.TabularInline):
    model = Modelo
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    inlines = [
        ModelosInline
    ]
    list_display = ('nome','preco','preco_promocional',
                    'estoque','publico','categoria')
    list_display_links = ('nome','categoria')
    list_editable = ('preco','preco_promocional','estoque','publico',)
    list_filter = ('publico','categoria')
    search_fields = ('nome','categoria')

admin.site.register(Produto,ProdutoAdmin)
admin.site.register(Modelo)
