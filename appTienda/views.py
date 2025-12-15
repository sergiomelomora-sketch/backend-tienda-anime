from django.shortcuts import render, get_object_or_404
from .models import Producto, Pedido


def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})


def seguimiento_pedido(request, token):
    pedido = get_object_or_404(Pedido, token_seguimiento=token)
    return render(request, 'seguimiento.html', {'pedido': pedido})
