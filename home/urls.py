from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categorias/', views.categoria, name='categoria'),  # Lista de categorias
    path('produtos/', views.lista_produtos, name='lista_produtos'),  # Lista de produtos
    path('formulario/<int:id>/', views.form_categoria, name='form_categoria'),
]
