import locale
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()


    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15,verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")


    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None

class Produto(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Produto")
    descricao = models.TextField(verbose_name="Descrição do Produto", default="Descrição padrão")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Produto", default=0.00)
    disponivel = models.BooleanField(default=True, verbose_name="Disponível para Venda")

    def __str__(self):
        return self.nome