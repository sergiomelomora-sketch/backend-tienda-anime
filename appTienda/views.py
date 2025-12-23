from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.dateparse import parse_date


from .models import (
    Producto,
    Pedido,
    Categoria,
    ImagenReferencia
)
from .forms import PedidoSolicitudForm


# =========================
# CATÁLOGO DE PRODUCTOS
# =========================
def catalogo(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    # Búsqueda por nombre o descripción
    query = request.GET.get('q')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )

    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        try:
            productos = productos.filter(categoria_id=categoria_id)
        except ValueError:
            pass

    # Separar productos destacados
    productos_destacados = productos.filter(destacado=True)
    productos_normales = productos.filter(destacado=False)

    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_seleccionada': categoria_id,
        'productos_destacados': productos_destacados,
        'productos_normales': productos_normales,
    }
    return render(request, 'catalogo.html', context)


# =========================
# DETALLE DE PRODUCTO
# =========================
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {
        'producto': producto
    })


# =========================
# SOLICITUD DE PEDIDO
# =========================
def solicitar_pedido(request, producto_id=None):
    producto_referencia = None

    if producto_id:
        producto_referencia = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = PedidoSolicitudForm(request.POST, request.FILES)

        if form.is_valid():
            # Transacción para asegurar consistencia
            with transaction.atomic():
                pedido = form.save(commit=False)
                pedido.producto = producto_referencia
                pedido.plataforma = 'sitio_web'
                pedido.estado = 'solicitado'
                pedido.estado_pago = 'pendiente'
                pedido.save()

                # Guardar múltiples imágenes de referencia
                imagenes = request.FILES.getlist('imagenes_referencia')
                for imagen_archivo in imagenes:
                    ImagenReferencia.objects.create(
                        pedido=pedido,
                        imagen=imagen_archivo
                    )

            return redirect(
                'confirmacion_pedido',
                token=pedido.token_seguimiento
            )
    else:
        form = PedidoSolicitudForm()

    context = {
        'form': form,
        'producto_referencia': producto_referencia
    }
    return render(request, 'solicitud_pedido.html', context)


# =========================
# CONFIRMACIÓN DE PEDIDO
# =========================
def confirmacion_pedido(request, token):
    pedido = get_object_or_404(Pedido, token_seguimiento=token)

    url_seguimiento = request.build_absolute_uri(
        reverse('seguimiento', kwargs={'token': token})
    )

    return render(request, 'confirmacion_pedido.html', {
        'pedido': pedido,
        'url_seguimiento': url_seguimiento
    })


# =========================
# SEGUIMIENTO DE PEDIDO
# =========================
def seguimiento_pedido(request, token):
    pedido = get_object_or_404(Pedido, token_seguimiento=token)
    return render(request, 'seguimiento.html', {
        'pedido': pedido
    })

@login_required
def reporte_pedidos(request):
    pedidos = Pedido.objects.all()

    # Filtros desde GET
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    plataforma = request.GET.get('plataforma')

    if fecha_inicio:
        pedidos = pedidos.filter(fecha_creacion__date__gte=parse_date(fecha_inicio))

    if fecha_fin:
        pedidos = pedidos.filter(fecha_creacion__date__lte=parse_date(fecha_fin))

    if plataforma:
        pedidos = pedidos.filter(plataforma=plataforma)

    # Agrupación por estado
    reporte = pedidos.values('estado').annotate(
        total=Count('id')
    ).order_by('estado')

    # Datos para gráfico
    estados = [item['estado'] for item in reporte]
    totales = [item['total'] for item in reporte]

    context = {
        'reporte': reporte,
        'estados': estados,
        'totales': totales,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'plataforma': plataforma,
        'plataformas': Pedido.PLATAFORMA,
    }

    return render(request, 'reporte_pedidos.html', context)

def catalogo(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    query = request.GET.get('q')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # 🔴 NUEVO: filtro por productos destacados
    destacados = request.GET.get('destacados')
    if destacados:
        productos = productos.filter(destacado=True)

    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_seleccionada': categoria_id,
        'destacados_activo': destacados,  # 👈 para el template
    }
    return render(request, 'catalogo.html', context)
