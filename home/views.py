from django.shortcuts import render, get_object_or_404, redirect
from .models import *  # Agora, ambos os modelos estão sendo importados
from .forms import *  # Certifique-se de ter os formulários para Categoria e Cliente
from django.contrib import messages
from django.core.paginator import Paginator

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

def excluir_cliente(request, id):
    try:
        cliente = get_object_or_404(Cliente, id=id)
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso.')
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
    return redirect('lista_cliente')
