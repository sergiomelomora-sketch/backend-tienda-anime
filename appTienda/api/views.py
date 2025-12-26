from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from appTienda.models import Insumo, Pedido
from appTienda.api.serializers import InsumoSerializer, PedidoSerializer

class InsumoViewSet(ModelViewSet):
    """
    Permite: Listar, Crear, Ver detalle, Modificar y Eliminar.
    """
    queryset = Insumo.objects.all().order_by("nombre")
    serializer_class = InsumoSerializer

class PedidoViewSet(mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    GenericViewSet):
    """
    API 2: Permite Crear (POST) y Modificar (PUT/PATCH).
    RESTRICCIÓN: Bloquea Listar (GET colección) y Eliminar (DELETE).
    """
    queryset = Pedido.objects.all().order_by("-fecha_creacion")
    serializer_class = PedidoSerializer

    @action(detail=False, methods=["get"], url_path="filtrar")
    def filtrar(self, request):
        queryset = self.get_queryset()
        desde = request.query_params.get("desde")
        hasta = request.query_params.get("hasta")
        estado = request.query_params.get("estado")
        max_res = request.query_params.get("max")

        if desde and hasta:
            try:
                queryset = queryset.filter(fecha_solicitada__range=[desde, hasta])
            except Exception:
                return Response(
                    {"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        if estado:
            estados_validos = [e[0] for e in Pedido.ESTADO_PEDIDO]
            if estado not in estados_validos:
                return Response(
                    {"error": f"Estado inválido. Use: {estados_validos}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(estado=estado)

        if max_res:
            try:
                limite = int(max_res)
                queryset = queryset[:limite]
            except ValueError:
                return Response(
                    {"error": "El parámetro 'max' debe ser un número entero."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)