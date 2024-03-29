# Generated by Django 4.1.6 on 2023-02-24 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0005_alter_pedido_qtd_valor_total_alter_pedido_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itempedido',
            old_name='preco_promo',
            new_name='preco_total_promo',
        ),
        migrations.RenameField(
            model_name='itempedido',
            old_name='preco',
            new_name='preco_total_unitario',
        ),
        migrations.AddField(
            model_name='itempedido',
            name='preco_unitario',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itempedido',
            name='preco_unitario_promo',
            field=models.FloatField(default=0),
        ),
    ]
