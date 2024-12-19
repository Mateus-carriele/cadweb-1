from django.shortcuts import render, get_object_or_404, redirect
from .models import *  # Agora, ambos os modelos estão sendo importados
from .forms import *  # Certifique-se de ter os formulários para Categoria e Cliente
from django.contrib import messages

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
    if id:
        categoria = get_object_or_404(Categoria, id=id)

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
    if id:
        cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente salvo com sucesso.')
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
    categoria = get_object_or_404(Categoria, id=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

# Detalhes do cliente 
def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'cliente/detalhes_cliente.html', {'cliente': cliente})
