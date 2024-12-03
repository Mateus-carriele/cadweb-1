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



def form_categoria(request, id):
    # Tenta encontrar o produto no banco de dados, se não encontrado, retorna 404
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        # Preenche o formulário com os dados do POST
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()  # Atualiza o produto no banco de dados
            return redirect('produtos')  # Redireciona para a listagem de produtos
    else:
        # Preenche o formulário com os dados do produto para edição
        form = ProdutoForm(instance=produto)

    return render(request, 'produto/editar.html', {'form': form})
