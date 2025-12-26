from rest_framework import serializers
from appTienda.models import Insumo, Pedido
from django.utils import timezone

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = [
            "id", 
            "nombre", 
            "tipo", 
            "cantidad_disponible", 
            "unidad", 
            "marca", 
            "color"
        ]

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__' 

    def validate_fecha_solicitada(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Error 400: La fecha de entrega no puede ser una fecha pasada.")
        return value