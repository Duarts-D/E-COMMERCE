# Generated by Django 4.1.6 on 2023-02-23 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0002_alter_itempedido_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itempedido',
            old_name='quantidae',
            new_name='quantidade',
        ),
    ]
