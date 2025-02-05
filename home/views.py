from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
import base64
from django.http import JsonResponse
from django.apps import apps
from django.db.models import Q

# Página inicial
def index(request):
    return render(request, 'index.html')

# Lista de categorias
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
            return redirect('categoria')

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
            return redirect('lista_cliente')

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
        messages.error(request, 'Registro não encontrado.')
        return redirect('categoria')
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

# Detalhes do cliente
def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('lista_cliente')
    return render(request, 'cliente/detalhes_cliente.html', {'cliente': cliente})

# Listar produtos
def listar_produtos(request):
    produtos = Produto.objects.all().order_by('valor')
    return render(request, 'produto/lista.html', {'produtos': produtos})

# Criar ou editar produto
def form_produto(request, id=None):
    produto = None
    if id:  # Verifica se o ID foi passado para edição
        try:
            produto = Produto.objects.get(id=id)
        except Produto.DoesNotExist:
            messages.error(request, 'Produto não encontrado.')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            if id:
                messages.success(request, 'Produto atualizado com sucesso.')
            else:
                messages.success(request, 'Produto criado com sucesso.')
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produto/formulario.html', {'form': form})

# Excluir produto
def excluir_produto(request, id):
    try:
        produto = get_object_or_404(Produto, id=id)
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
    except Produto.DoesNotExist:
        messages.error(request, 'Produto não encontrado.')
    return redirect('listar_produtos')

# Detalhes do produto
def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado.')
        return redirect('listar_produtos')
    return render(request, 'produto/detalhes.html', {'produto': produto})

# Ajustar estoque
def ajustar_estoque(request, id):
    produto = Produto.objects.get(pk=id)
    estoque = produto.estoque
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            return render(request, 'produto/detalhes.html', {'form': form})
    else:
        form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form})

# Buscar dados
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '')
    try:
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)

    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)

    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

# Páginas de teste
def testes1(request):
    return render(request, 'testes/testes1.html')

def testes2(request):
    return render(request, 'testes/testes2.html')

def teste3(request):
    return render(request, 'testes/teste3.html')

# Listar pedidos
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})
    
def remover_pedido(request, id):
    try:
        pedido = get_object_or_404(Pedido, pk=id)
        pedido.delete()  # Remove o pedido
        messages.success(request, 'Pedido removido com sucesso!')
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido não encontrado.')

    return redirect('pedido')  # Redireciona para a lista de pedidos

# Novo pedido
def novo_pedido(request, cliente_id):
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

# Detalhes do pedido
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
    else: # method Post
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False) # commit=False retorna o objeto item_pedido vindo do form para fazermos modificações adicionais antes de salvá-la, colocar o preço do produto, verificar estoque.
            item_pedido.preco = item_pedido.produto.valor # acessando o produto do relacionamento
            # realizar aqui o tratamento do estoque, para isso
            # Pegar o estoque (item_pedido.produto.estoque do relacionamento) atual 
            # verificar se a quantidade (item_pedido.produto.estoque.qtde) é suficiente para o item solicitado (tem_pedido.qtde)
            # Se não houver estoque suficiente, você pode adicionar uma mensagem de erro e não salvar a operação
            # Se sim, decrementar a quantidade do item no estoque do produto e salvar os objetos estoque e item_pedido
            item_pedido.save()
        else:
             messages.error(request, 'Erro ao adicionar produto')
                  
    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html',contexto )


# Remover item do pedido
def remover_item_pedido(request, item_id):
    try:
        item_pedido = ItemPedido.objects.get(pk=item_id)  # Usa item_id ao invés de id
    except ItemPedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=item_id)
    
    pedido_id = item_pedido.pedido.id  # Armazena o ID do pedido antes de remover o item
    estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
    estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
    estoque.save()  # Salva as alterações no estoque
    # Remove o item do pedido
    item_pedido.delete()
    messages.success(request, 'Operação realizada com Sucesso')

    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhes_pedido', id=pedido_id)

# Adicionar item ao pedido
def adicionar_item_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido

            produto = item.produto
            estoque = produto.estoque
            if estoque.qtde < item.qtde:
                messages.error(request, 'Estoque insuficiente!')
                return redirect('detalhes_pedido', id=pedido_id)

            item.preco = produto.valor
            estoque.qtde -= item.qtde
            estoque.save()

            item.save()
            messages.success(request, 'Item adicionado com sucesso!')
            return redirect('detalhes_pedido', id=pedido_id)
    else:
        form = ItemPedidoForm()

    return render(request, 'pedido/adicionar_item.html', {'form': form, 'pedido': pedido})

# Editar item do pedido
def editar_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)
         
    pedido = item_pedido.pedido  # Acessa o pedido diretamente do item
    quantidade_anterior = item_pedido.qtde  # Armazena a quantidade anterior
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)  # prepara a instância do item_pedido sem persistir ainda
            print(item_pedido.produto.id)
            # realizar aqui o tratamento do estoque
            # Pegar a nova quantidade do item pedido
            # Obtém o estoque atual do produto
            # Verifica se há estoque suficiente para a nova quantidade
            # Se não mostras msg Quantidade em estoque insuficiente para o produto.
            # Se sim
            # Pegar a quantidade anterior ao estoque
            # Decrementa a nova quantidade do estoque
            # Salva as alterações no estoque
            # Salva o item do pedido após ajustar o estoque
            item_pedido.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('detalhes_pedido', id=pedido.id)
    else:
        form = ItemPedidoForm(instance=item_pedido)
        
    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido,
    }
    return render(request, 'pedido/detalhes.html', contexto)
