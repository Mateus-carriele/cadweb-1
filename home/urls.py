from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name="index"),
  
   path('buscar_dados/<str:app_modelo>/', views.buscar_dados, name='buscar_dados'),

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


    path('buscar_dados/<str:app_modelo>', views.buscar_dados, name='buscar_dados'),
    path('testes1', views.testes1, name='testes1'),
    path('testes2', views.testes2, name='testes2'),
    path('teste3', views.teste3, name='teste3'),



    path('pedidos/', views.pedido, name='pedido'),
    path('pedido/novo/<int:cliente_id>/', views.novo_pedido, name='novo_pedido'),
    path('pedido/detalhes/<int:id>/', views.detalhes_pedido, name='detalhes_pedido'),
    path('pedido/<int:pedido_id>/adicionar_item/', views.adicionar_item_pedido, name='adicionar_item_pedido'),
    path('pedido/editar_item/<int:item_id>/', views.editar_item_pedido, name='editar_item_pedido'),
    path('pedido/remover_item/<int:item_id>/', views.remover_item_pedido, name='remover_item_pedido'),

  
]
