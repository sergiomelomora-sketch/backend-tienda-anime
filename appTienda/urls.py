#hecho por el equipo
from django.urls import path
from . import views
from .views import reporte_pedidos


urlpatterns = [
    
    path('', views.catalogo, name='catalogo'),
    
    
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    
    
    path('solicitar/', views.solicitar_pedido, name='solicitar_pedido_sin_producto'),
    
    
    path('solicitar/<int:producto_id>/', views.solicitar_pedido, name='solicitar_pedido_con_producto'),
    
    
    path('confirmacion/<uuid:token>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    
    
    path('seguimiento/<uuid:token>/', views.seguimiento_pedido, name='seguimiento'),
    
    path('reporte/', reporte_pedidos, name='reporte_pedidos'),

]