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
    # Recupera a instância de Produto ou Estoque
    produto = get_object_or_404(Produto, pk=id)  # Aqui você deve buscar pelo ID do produto, por exemplo
    estoque_item, created = Estoque.objects.get_or_create(produto=produto, defaults={'qtde': 0})

    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque_item)
        if form.is_valid():
            form.save()  # Salva as alterações no estoque
            return redirect('detalhes_produto', id=produto.id)  # Redireciona para os detalhes do produto
    else:
        form = EstoqueForm(instance=estoque_item)  # Preenche o formulário com a instância do estoque

    return render(request, 'produto/estoque.html', {'form': form, 'produto': produto})
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
    else:  # método POST
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)  # commit=False retorna o objeto item_pedido vindo do form para fazermos modificações adicionais antes de salvá-la
            item_pedido.preco = item_pedido.produto.valor  # acessando o produto do relacionamento

            # Verificação de estoque
            estoque_atual = item_pedido.produto.estoque  # A quantidade em estoque do produto
            if item_pedido.qtde > estoque_atual:
                messages.error(request, f"Estoque insuficiente para o produto {item_pedido.produto.nome}.")
                return redirect('detalhes_pedido', id=id)

            # Decrementa a quantidade do item no estoque (se houver estoque suficiente)
            estoque_item, created = Estoque.objects.get_or_create(produto=item_pedido.produto, defaults={'qtde': 0})
            estoque_item.qtde -= item_pedido.qtde  # Reduz a quantidade no estoque
            estoque_item.save()

            # Salva o item no pedido
            item_pedido.save()
            messages.success(request, 'Produto adicionado ao pedido com sucesso!')
        else:
            messages.error(request, 'Erro ao adicionar produto ao pedido')
                  
    contexto = {
        'pedido': pedido,
        'form': form,
        'total_pedido': pedido.total,  # Adiciona o total do pedido
        'total_pago': pedido.total_pago,  # Adiciona o total pago
        'debito': pedido.debito,  # Adiciona o débito
    }
    return render(request, 'pedido/detalhes.html', contexto)

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
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)

    pedido = item_pedido.pedido  # Pedido relacionado ao item
    quantidade_anterior = item_pedido.qtde  # Salva a quantidade anterior

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)  # Obtém a instância sem salvar no banco

            produto = item_pedido.produto  # Produto relacionado ao item
            nova_quantidade = item_pedido.qtde  # Nova quantidade informada no formulário

            estoque_atual = produto.estoque  # Estoque atual do produto

            # Verifica se a nova quantidade está disponível no estoque
            if nova_quantidade > quantidade_anterior:  # Se aumentou a quantidade do pedido
                diferenca = nova_quantidade - quantidade_anterior
                if diferenca > estoque_atual:
                    messages.error(request, f"Quantidade insuficiente em estoque para o produto {produto.nome}.")
                    return redirect('editar_item_pedido', id=id)
                else:
                    # Reduz o estoque utilizando o método de atualização
                    produto.atualizar_estoque(estoque_atual - diferenca)
            elif nova_quantidade < quantidade_anterior:  # Se reduziu a quantidade do pedido
                diferenca = quantidade_anterior - nova_quantidade
                # Reabastece o estoque utilizando o método de atualização
                produto.atualizar_estoque(estoque_atual + diferenca)

            item_pedido.save()  # Salva o item do pedido

            messages.success(request, 'Item atualizado com sucesso!')
            return redirect('detalhes_pedido', id=pedido.id)
    else:
        form = ItemPedidoForm(instance=item_pedido)

    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido,
    }
    return render(request, 'pedido/detalhes.html', contexto)




def form_pagamento(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso')
    else:
        pagamento = Pagamento(pedido=pedido)
        form = PagamentoForm(instance=pagamento)

    contexto = {
        'form': form,
        'pedido': pedido,  # Certifique-se de que o pedido está sendo passado
    }
    return render(request, 'pedido/pagamento.html', contexto)

def editar_pagamento(request, id):
    try:
        pagamento = Pagamento.objects.get(pk=id)
    except Pagamento.DoesNotExist:
        messages.error(request, 'Pagamento não encontrado')
        return redirect('detalhes_pedido', id=id)

    pedido = pagamento.pedido  # Pedido relacionado ao pagamento
    valor_anterior = pagamento.valor  # Salva o valor anterior do pagamento

    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            pagamento = form.save(commit=False)  # Obtém a instância sem salvar no banco
            novo_valor = pagamento.valor  # Novo valor informado no formulário

            total_pedido = pedido.total  # Total do pedido
            total_pago = pedido.total_pago - valor_anterior + novo_valor  # Recalcula total pago

            # Verifica se o pagamento excede o valor do pedido
            if total_pago > total_pedido:
                messages.error(request, "O valor total pago não pode ser maior que o total do pedido.")
                return redirect('editar_pagamento', id=id)

            pagamento.save()  # Salva o pagamento atualizado

            messages.success(request, 'Pagamento atualizado com sucesso!')
            return redirect('detalhes_pedido', id=pedido.id)
    else:
        form = PagamentoForm(instance=pagamento)

    contexto = {
        'pedido': pedido,
        'form': form,
        'pagamento': pagamento,
    }
    return render(request, 'pedido/editar_pagamento.html', contexto)

def excluir_pagamento(request, id):
    try:
        pagamento = get_object_or_404(Pagamento, pk=id)
        pedido = pagamento.pedido  # Obtém o pedido antes de excluir
        pagamento.delete()  # Remove o pagamento
        messages.success(request, 'Pagamento removido com sucesso!')
    except Pagamento.DoesNotExist:
        messages.error(request, 'Pagamento não encontrado.')

    return redirect('detalhes_pedido', id=pedido.id)
def remover_item_pedido(request, id):
    try:
        item_pedido = get_object_or_404(ItemPedido, pk=id)
        pedido = item_pedido.pedido  # Obtém o pedido antes de excluir
        item_pedido.delete()  # Remove o item do pedido
        messages.success(request, 'Item removido com sucesso!')
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Item não encontrado.')

    return redirect('detalhes_pedido', id=pedido.id) 