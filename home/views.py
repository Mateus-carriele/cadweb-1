from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

def index(request):
    return render(request, 'index.html')

def categoria(request):
    # Exibe a lista de categorias
    contexto = {
        'lista': Categoria.objects.all().order_by('id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def lista_produtos(request):
    # Exibe a lista de produtos
    lista = Categoria.objects.all()  
    return render(request, 'categoria/lista.html', {'lista': lista})



def form_categoria(request, id=None):
    if id:  # Se o ID for fornecido, tenta buscar o registro
        categoria = get_object_or_404(Categoria, id=id)
    else:  # Se não, cria uma nova instância
        categoria = None

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()  # Salva no banco de dados
            return redirect('categoria')  # Redireciona para a listagem
    else:
        form = CategoriaForm(instance=categoria)  # Formulário com a instância existente ou vazio

    return render(request, 'categoria/formulario.html', {'form': form})

def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('categoria')  # Redireciona para a listagem de categorias

def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})