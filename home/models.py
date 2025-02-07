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
        return estoque_item.qtde  # Retorna a quantidade atual em estoque

    def atualizar_estoque(self, quantidade):
        """
        Atualiza o estoque do produto diretamente.
        Passa a quantidade a ser adicionada ou subtraída.
        """
        estoque_item, created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        estoque_item.qtde = quantidade
        estoque_item.save()

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

class Pedido(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[(1, 'Novo'), (2, 'Em Andamento'), (3, 'Concluído'), (4, 'Cancelado')], default=1)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome} ({self.data_pedido.strftime('%d/%m/%Y')})"

    @property
    def pagamentos(self):
        """Retorna todos os pagamentos associados a este pedido."""
        return self.pagamento_set.all()

    @property
    def total(self):
        """Calcula o total de todos os itens no pedido."""
        return sum(item.qtde * item.valor for item in self.itempedido_set.all())

    @property
    def total_pago(self):
        """Calcula o total de todos os pagamentos do pedido."""
        return sum(pagamento.valor for pagamento in self.pagamentos)

    @property
    def debito(self):
        """Calcula o débito do pedido (total - total pago)."""
        return self.total - self.total_pago

    @property
    def data_pedidof(self):
        """Retorna a data formatada no padrão DD/MM/AAAA HH:MM."""
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return "Data não disponível"

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
        return f'{self.produto.nome} - {self.qtde} - {self.valor}'  # Indentação corrigida

    def calcular_valor(self):
        return self.produto.valor * self.qtde

    @property
    def total(self):
        return self.qtde * self.valor


class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4


    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]


    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None
