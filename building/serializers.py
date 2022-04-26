
from rest_framework import serializers

from .models import Building

class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ['id', 'type', 'level', 'hp', 'started_at', 'finished_at', ]
        depth = 1
