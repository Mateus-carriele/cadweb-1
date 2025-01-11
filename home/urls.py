from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name="index"),
  


    # Categorias
    path('categorias/', views.categoria, name='categoria'),  # Lista de categorias
    path('formulario/', views.form_categoria, name='form_categoria'),  # Criação de categoria
    path('formulario/<int:id>/', views.form_categoria, name='form_categoria'),  # Edição de categoria
    path('categorias/excluir/<int:id>/', views.excluir_categoria, name='excluir_categoria'),  # Excluir categoria
    path('categoria/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),  # Detalhes da categoria

    # Clientes
    path('clientes/', views.lista_cliente, name='lista_cliente'),  # Lista de clientes
    path('form_cliente/', views.form_cliente, name='form_cliente'),  # Criação de cliente
    path('form_cliente/<int:id>/', views.form_cliente, name='form_cliente'),  # Edição de cliente
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),  # Excluir cliente
    path('cliente/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),  # Detalhes do cliente



    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/novo/', views.form_produto, name='form_produto'),
    path('produtos/<int:id>/editar/', views.form_produto, name='editar_produto'),
    path('produtos/<int:id>/excluir/', views.excluir_produto, name='excluir_produto'),
    path('produtos/detalhes/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    path('ajustar_estoque/<int:id>', views.ajustar_estoque, name='ajustar_estoque'),
    
  
]
