from django.db import models
import locale
import base64
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")

    def __str__(self):
        return self.nome

    @property
    def datanascimento(self):
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    img_base64 = models.TextField(blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    @property
    def estoque(self):
        estoque_item, created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

class Pedido(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[(1, 'Novo'), (2, 'Em Andamento'), (3, 'Concluído'), (4, 'Cancelado')], default=1)
    
    @property
    def total(self):
        """Calcula o total de todos os itens no pedido, formatado como moeda local"""
        total = sum(item.qtde * item.valor for item in self.itempedido_set.all())  # Altere 'preco' para 'valor'
        return total

    @property
    def qtdeItens(self):
        """Conta a qtde de itens no pedido"""
        return self.itempedido_set.count()  


from django.db import models

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()  # Campo para a quantidade de produtos
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.valor:
            self.valor = self.produto.valor * self.qtde  # Calcula o valor com base no produto e na quantidade
        super().save(*args, **kwargs)  # Salva o ItemPedido

    def __str__(self):
        return f'{self.produto.nome} - {self.qtde} - {self.valor}'

    def calcular_valor(self):
        return self.produto.valor * self.qtde
    def __str__(self):
        return f'{self.produto.nome} - {self.qtde}'
        
    @property
    def total(self):
        return self.qtde * self.valor

