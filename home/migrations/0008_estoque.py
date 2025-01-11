# Generated by Django 4.2.16 on 2025-01-09 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_produto_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtde', models.IntegerField(verbose_name='Quantidade')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.produto', verbose_name='Produto')),
            ],
        ),
    ]
