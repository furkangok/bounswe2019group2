from rest_framework import serializers
from ..models import Equipment


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipment
        fields = ["url", "id", "name", "category", "symbol"]
