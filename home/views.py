from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages

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
    if id:  # Verifica se o ID foi passado para edição
        try:
            categoria = Categoria.objects.get(id=id)
        except Categoria.DoesNotExist:
            messages.error(request, 'A categoria que você tentou editar não foi encontrada.')
            return redirect('categoria')  # Redireciona para a listagem de categorias
    else:
        categoria = None  # Novo registro

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria salva com sucesso.')
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categoria/formulario.html', {'form': form})

def excluir_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso.')
    except Categoria.DoesNotExist:
        messages.error(request, 'A categoria que você tentou excluir não foi encontrada.')
    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao tentar excluir a categoria: {e}')
    return redirect('categoria')  # Redireciona para a listagem de categorias

def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'A categoria que você tentou visualizar não foi encontrada.')
        return redirect('categoria')  # Redireciona para a listagem de categorias
    # Se a categoria for encontrada, renderiza o template
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})