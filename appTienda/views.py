from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q 
from .models import Producto, Pedido, Categoria, ImagenReferencia
from .forms import PedidoSolicitudForm 


# hecho por el equipo 
def catalogo(request):
    
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    # IA(chatgpt)
    query = request.GET.get('q')
    if query:
        
        productos = productos.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))

    # hecho por el equipo con dudas preguntadas a chatgpt sobre que comandos usar
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        try:
            
            productos = productos.filter(categoria_id=categoria_id)
        except ValueError:
            
            pass
            
    
    productos_destacados = productos.filter(destacado=True)
    productos_normales = productos.filter(destacado=False)
    #hecho por el equipo
    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_seleccionada': categoria_id,
        'productos_destacados': productos_destacados,
        'productos_normales': productos_normales,
    }
    return render(request, 'catalogo.html', context)


# mezcla de equipo e IA (chatgpt)
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})


# mezcla de equipo e IA(chatgpt)
def solicitar_pedido(request, producto_id=None):
    producto_referencia = None
    
    
    if producto_id:
        producto_referencia = get_object_or_404(Producto, id=producto_id)
        
    if request.method == 'POST':
        form = PedidoSolicitudForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            pedido = form.save(commit=False)
            
            
            pedido.producto = producto_referencia 
            
            
            pedido.plataforma = 'sitio_web' 
            
            # mezcla de IA y equipo
            pedido.estado = 'solicitado'
            pedido.estado_pago = 'pendiente'
            
            pedido.save() 

            
            imagenes = request.FILES.getlist('imagenes_referencia')
            for imagen_archivo in imagenes:
                
                ImagenReferencia.objects.create(pedido=pedido, imagen=imagen_archivo)
                
            
            return redirect('confirmacion_pedido', token=pedido.token_seguimiento)
            
    else:
        
        form = PedidoSolicitudForm()
        
    context = {
        'form': form,
        'producto_referencia': producto_referencia
    }
    
    return render(request, 'solicitud_pedido.html', context)


# mezcla de equipo y IA(chatgpt)
def confirmacion_pedido(request, token):
    pedido = get_object_or_404(Pedido, token_seguimiento=token)
    
    
    url_seguimiento = request.build_absolute_uri(
        reverse('seguimiento', kwargs={'token': token})
    )
    
    return render(request, 'confirmacion_pedido.html', {
        'pedido': pedido, 
        'url_seguimiento': url_seguimiento
    })


# hecho por el equipo
def seguimiento_pedido(request, token):
    pedido = get_object_or_404(Pedido, token_seguimiento=token)
    return render(request, 'seguimiento.html', {'pedido': pedido})