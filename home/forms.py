from django import forms
from .models import *
from datetime import date
import base64

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': 'Ordem'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem <= 0:
            raise forms.ValidationError("O campo ordem deve ser maior que zero.")
        return ordem

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(
                attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'
            ),  # Parêntese fechado corretamente
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 5:
            raise forms.ValidationError("O nome deve ter pelo menos 5 caracteres.")
        return nome

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > date.today():
            raise forms.ValidationError('A data de nascimento não pode ser no futuro!')
        return datanasc

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'valor', 'categoria', 'img_base64']
        widgets = {
            'categoria': forms.HiddenInput(),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'img_base64': forms.HiddenInput(),
            'valor': forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }
        labels = {
            'nome': 'Nome do Produto',
            'valor': 'Preço do Produto',
        }

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['valor'].localize = True
        self.fields['valor'].widget.is_localized = True

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise forms.ValidationError('Categoria não encontrada.')
        return categoria

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 5:
            raise forms.ValidationError("O nome deve ter pelo menos 5 caracteres.")
        return nome

    def is_img_base64_valid(self):
        try:
            if self.cleaned_data['img_base64']:
                base64.b64decode(self.cleaned_data['img_base64'])
                return True
            return False
        except base64.binascii.Error:
            return False

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'qtde']
        widgets = {
            'produto': forms.HiddenInput(),
            'qtde': forms.TextInput(attrs={'class': 'inteiro form-control', 'placeholder': 'Quantidade'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput(),
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido', 'produto', 'qtde', ]
        widgets = {
            'pedido': forms.HiddenInput(),
            'produto': forms.HiddenInput(),
            'qtde': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_qtde(self):
        qtde = self.cleaned_data.get('qtde')
        if qtde <= 0:
            raise forms.ValidationError('A quantidade deve ser maior que zero.')
        return qtde

    def save(self, commit=True):
        item = super().save(commit=False)
        item.valor = item.produto.valor * item.qtde  # Atribui o valor total com base no produto e quantidade
        if commit:
            item.save()
        return item



class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pedido','forma','valor']
        widgets = {
            'pedido': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            # Usando Select para renderizar as opções
            'forma': forms.Select(attrs={'class': 'form-control'}),  
            'valor':forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
         }
        
    def __init__(self, *args, **kwargs):
            super(PagamentoForm, self).__init__(*args, **kwargs)
            self.fields['valor'].localize = True
            self.fields['valor'].widget.is_localized = True      
