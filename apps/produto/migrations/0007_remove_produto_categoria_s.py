# Generated by Django 4.1.6 on 2023-03-01 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_produto_categoria_s'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='categoria_s',
        ),
    ]
