from django.shortcuts import render, get_object_or_404, redirect
from .models import *  # Agora, ambos os modelos estão sendo importados
from .forms import *  # Certifique-se de ter os formulários para Categoria e Cliente
from django.contrib import messages
from django.core.paginator import Paginator
import base64
from django.http import JsonResponse
from django.apps import apps
from django.db.models import Q


def index(request):
    return render(request, 'index.html')




    
def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('id'),
    }
    return render(request, 'categoria/lista.html', contexto)

# Lista de clientes
def lista_cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('id'),
    }
    return render(request, 'cliente/lista_cliente.html', contexto)

# Formulário para criar ou editar categoria
def form_categoria(request, id=None):
    categoria = None
    if id:  # Editar categoria existente
        try:
            categoria = Categoria.objects.get(id=id)
        except Categoria.DoesNotExist:
            messages.error(request, 'Categoria não encontrada.')
            return redirect('categoria')  # Redireciona para a lista de categorias

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria salva com sucesso.')
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categoria/formulario.html', {'form': form})


# Formulário para criar ou editar cliente
def form_cliente(request, id=None):
    cliente = None
    if id:  # Verifica se o ID foi passado para edição
        try:
            cliente = Cliente.objects.get(id=id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')
            return redirect('lista_cliente')  # Redireciona para a lista de clientes

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            if id:
                messages.success(request, 'Cliente atualizado com sucesso.')
            else:
                messages.success(request, 'Cliente criado com sucesso.')
            return redirect('lista_cliente')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'cliente/formulario_cliente.html', {'form': form})

# Excluir categoria
def excluir_categoria(request, id):
    try:
        categoria = get_object_or_404(Categoria, id=id)
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso.')
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')
    return redirect('categoria')

# Excluir cliente
def excluir_cliente(request, id):
    try:
        cliente = get_object_or_404(Cliente, id=id)
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso.')
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
    return redirect('lista_cliente')

# Detalhes da categoria
def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        # Caso o registro não seja encontrado, exibe uma mensagem de erro
        messages.error(request, 'Registro não encontrado.')
        return redirect('categoria')  # Redireciona para a listagem de categorias
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

# Detalhes do cliente
def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('lista_cliente')  # Redireciona para a lista de clientes
    return render(request, 'cliente/detalhes_cliente.html', {'cliente': cliente})
    



    # Listar produtos
def listar_produtos(request):
    produtos = Produto.objects.all().order_by('valor')  # Ordenar por valor
    return render(request, 'produto/lista.html', {'produtos': produtos})
# Criar ou editar produto
def form_produto(request, id=None):
    produto = None
    if id:  # Verifica se o ID foi passado para edição
        try:
            produto = Produto.objects.get(id=id)  # Corrigido o nome do modelo (Produto)
        except Produto.DoesNotExist:
            messages.error(request, 'Produto não encontrado.')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            if id:  # Corrigido o alinhamento da indentação
                messages.success(request, 'Produto atualizado com sucesso.')
            else:
                messages.success(request, 'Produto criado com sucesso.')
            
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
        
    produtos = Produto.objects.all().order_by('valor')

    return render(request, 'produto/formulario.html', {'form': form})


# Excluir produto
def excluir_produto(request, id):
    try:     
        produto = get_object_or_404(Produto, id=id)
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
    except  produto.DoesNotExist:
        messages.error(request, 'Produto não encontrado.')

    return redirect('listar_produtos')


# Detalhes do produtos
def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        # Caso o registro não seja encontrado, exibe uma mensagem de erro
        messages.error(request, 'Registro não encontrado.')
        return redirect('listar_produtos')  # Certifique-se de que 'listar_produtos' está configurado em urls.py
    return render(request, 'produto/detalhes.html', {'produto': produto})


def ajustar_estoque(request, id):
    produto = Produto.objects.get(pk=id)
    estoque = produto.estoque # pega o objeto estoque relacionado ao produto
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            return render(request, 'produto/detalhes.html', {'form': form,})
    else:
         form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form,})


def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)




def testes1(request):
    return render(request, 'testes/testes1.html')
    
def testes2(request):
    return render(request, 'testes/testes2.html')

def teste3(request):
    return render(request, 'testes/teste3.html')




def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})


def novo_pedido(request, cliente_id):  # Alterado de 'id' para 'cliente_id'
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente')  
        
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido/form.html', {'form': form})
    
    else:  
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('pedido')


def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    
    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else:
        form = ItemPedidoForm(request.POST)
        # aguardando implementação POST, salvar item
    
    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html',contexto )




def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)
    
    pedido_id = item_pedido.pedido.id  # Armazena o ID do pedido antes de remover o item
    estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
    estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
    estoque.save()  # Salva as alterações no estoque
    # Remove o item do pedido
    item_pedido.delete()
    messages.success(request, 'Operação realizada com Sucesso')


    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhes_pedido', id=pedido_id)



def adicionar_item_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido

            # Verifica o estoque
            produto = item.produto
            estoque = produto.estoque
            if estoque.qtde < item.qtde:
                messages.error(request, 'Estoque insuficiente!')
                return redirect('detalhes_pedido', id=pedido_id)

            # Define o preço do produto
            item.preco = produto.valor

            # Atualiza o estoque
            estoque.qtde -= item.qtde
            estoque.save()

            # Salva o item no pedido
            item.save()
            messages.success(request, 'Item adicionado com sucesso!')
            return redirect('detalhes_pedido', id=pedido_id)
    else:
        form = ItemPedidoForm()

    return render(request, 'pedido/adicionar_item.html', {'form': form, 'pedido': pedido})




def editar_item_pedido(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id)
    pedido = item.pedido
    quantidade_anterior = item.qtde

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item)
        if form.is_valid():
            nova_quantidade = form.cleaned_data['qtde']
            produto = item.produto
            estoque = produto.estoque

            # Verifica se há estoque suficiente
            diferenca = nova_quantidade - quantidade_anterior
            if estoque.qtde < diferenca:
                messages.error(request, 'Estoque insuficiente para a nova quantidade!')
                return redirect('detalhes_pedido', id=pedido.id)

            # Atualiza o estoque
            estoque.qtde -= diferenca
            estoque.save()

            # Salva o item atualizado
            form.save()
            messages.success(request, 'Item atualizado com sucesso!')
            return redirect('detalhes_pedido', id=pedido.id)
    else:
        form = ItemPedidoForm(instance=item)

    return render(request, 'pedido/editar_item.html', {'form': form, 'item': item})




