from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import producto

class ProductoSerializars(serializers.ModelSerializer):
    class Meta:
        model = producto
        fields = (
            'nombre_producto',
            'origen_producto',
            'valor_producto',
            'estado_fk',
        )






#Aqui se traspasan los datos a json o al reves 



