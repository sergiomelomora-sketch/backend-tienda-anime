from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('seguimiento/<uuid:token>/', views.seguimiento_pedido, name='seguimiento'),
]
