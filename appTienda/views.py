from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q, Count
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError

from .models import (
    Producto,
    Pedido,
    Categoria,
    ImagenReferencia
)
from .forms import PedidoSolicitudForm

def catalogo(request):
    token_busqueda = request.GET.get('buscar_pedido')
    if token_busqueda:
        try:
            token_limpio = token_busqueda.strip()
            pedido_encontrado = Pedido.objects.get(token_seguimiento=token_limpio)
            return redirect('seguimiento', token=pedido_encontrado.token_seguimiento)
        except (Pedido.DoesNotExist, ValidationError):
            pass

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    query = request.GET.get('q')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    producto_destacado_real = Producto.objects.annotate(
        total_pedidos=Count('pedido')
    ).order_by('-total_pedidos').first()

    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_seleccionada': categoria_id,
        'producto_destacado': producto_destacado_real,
    }
    return render(request, 'catalogo.html', context)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

def solicitar_pedido(request, producto_id=None):
    producto_referencia = None
    if producto_id:
        producto_referencia = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = PedidoSolicitudForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                pedido = form.save(commit=False)
                pedido.producto = producto_referencia
                pedido.plataforma = 'sitio_web'
                pedido.estado = 'solicitado'
                pedido.estado_pago = 'pendiente'
                pedido.save()

                imagenes = request.FILES.getlist('imagenes_referencia')
                for imagen_archivo in imagenes:
                    ImagenReferencia.objects.create(pedido=pedido, imagen=imagen_archivo)

            return redirect('confirmacion_pedido', token=pedido.token_seguimiento)
    else:
        form = PedidoSolicitudForm()

    return render(request, 'solicitud_pedido.html', {'form': form, 'producto_referencia': producto_referencia})


def confirmacion_pedido(request, token):
    pedido = get_object_or_404(Pedido, token_seguimiento=token)
    url_seguimiento = request.build_absolute_uri(reverse('seguimiento', kwargs={'token': token}))
    return render(request, 'confirmacion_pedido.html', {'pedido': pedido, 'url_seguimiento': url_seguimiento})

def seguimiento_pedido(request, token):
    pedido = get_object_or_404(Pedido, token_seguimiento=token)
    return render(request, 'seguimiento.html', {'pedido': pedido})


@login_required
def reporte_pedidos(request):
    pedidos_base = Pedido.objects.all().order_by('-fecha_solicitada')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    plataforma = request.GET.get('plataforma')

    if fecha_inicio:
        pedidos_base = pedidos_base.filter(fecha_solicitada__gte=parse_date(fecha_inicio))
    if fecha_fin:
        pedidos_base = pedidos_base.filter(fecha_solicitada__lte=parse_date(fecha_fin))
    
    if plataforma and plataforma != 'Todas':
        pedidos_base = pedidos_base.filter(plataforma=plataforma)

    reporte = pedidos_base.values('estado').annotate(total=Count('id')).order_by('estado')
    
    productos_top = pedidos_base.values('producto__nombre').annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')[:5]
    
    estados_labels = [item['estado'].capitalize() for item in reporte]
    totales_data = [item['total'] for item in reporte]

    context = {
        'pedidos': pedidos_base,      
        'reporte': reporte,           
        'productos_top': productos_top, 
        'estados': estados_labels,    
        'totales': totales_data,      
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'plataforma_sel': plataforma,
        'plataformas': Pedido.PLATAFORMA, 
    }
    return render(request, 'reporte_pedidos.html', context)