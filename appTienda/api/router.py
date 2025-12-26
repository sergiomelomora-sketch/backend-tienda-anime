from rest_framework.routers import DefaultRouter
from appTienda.api.views import InsumoViewSet , PedidoViewSet

router_insumo = DefaultRouter()
router_insumo.register(r"insumos", InsumoViewSet, basename="insumo")
router_insumo.register(r'pedidos', PedidoViewSet, basename='pedido')