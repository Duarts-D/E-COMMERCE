# Generated by Django 4.1.6 on 2023-03-07 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0004_alter_perfil_usuario_data_de_nascimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil_usuario',
            name='data_de_nascimento',
            field=models.DateField(),
        ),
    ]