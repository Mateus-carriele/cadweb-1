import locale
from django.db import models
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
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None


class Produto(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Produto")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Produto", default=0.00)
    img_base64 = models.TextField(blank=True, verbose_name="Imagem Base64")
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, verbose_name="Categoria")
    
    def __str__(self):
        return self.nome
    
    @property
    def estoque(self):
        # Tenta buscar o estoque; se não existir, cria um novo com quantidade zero
        estoque_item, created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item

                                                     

    @property
    def valor_formatado(self):
        """Retorna o valor formatado em moeda local."""
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(self.valor, grouping=True)

    def clean(self):
        """Valida os dados antes de salvar."""
        if self.valor < 0:
            raise ValidationError('O valor do produto não pode ser negativo.')

    def is_img_base64_valid(self):
        """Verifica se img_base64 contém dados válidos."""
        try:
            if self.img_base64:
                base64.b64decode(self.img_base64)
                return True
            return False
        except base64.binascii.Error:
            return False

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    qtde = models.IntegerField(verbose_name="Quantidade")

    def __str__(self):
        return f"{self.produto.nome} - {self.qtde} unidades"

class Pedido(models.Model):
    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4

    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None

    @property
    def total(self):
        """Calcula o total de todos os itens no pedido, formatado como moeda local"""
        total = sum(item.qtde * item.preco for item in self.itempedido_set.all())
        return total


    
    @property
    def qtdeItens(self):
        """Conta a qtde de itens no pedido, """
        return self.itempedido_set.count()  


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"      
