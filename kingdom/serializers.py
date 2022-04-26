from rest_framework import serializers

from building.models import Building
from .models import Kingdom, Resource, Location

class LocationSerializer(serializers.ModelSerializer):
    coordinateX = serializers.IntegerField(source='x')
    coordinateY = serializers.IntegerField(source='y')
    class Meta:
        model = Location
        fields = ['coordinateX', 'coordinateY']


class ResourceSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    updatedAt = serializers.IntegerField(source='updated_at')

    class Meta:
        model = Resource
        fields = ['type', 'amount', 'generation', 'updatedAt']


class KingdomSerializer(serializers.ModelSerializer):
    kingdomId = serializers.IntegerField(source='id')
    kingdomName = serializers.CharField(source='kingdom_name')
    ruler = serializers.CharField(source='player')
    population = serializers.SerializerMethodField()
    location = LocationSerializer()

    class Meta:
        model = Kingdom
        fields = ['kingdomId', 'kingdomName', 'ruler', 'population', 'location']
        depth = 1

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_population(self,instance):
        buildings = Building.objects.filter(kingdom_id = instance.id)
        sum_of_levels = 0

        for building in buildings:
            sum_of_levels += building.level

        return sum_of_levels
