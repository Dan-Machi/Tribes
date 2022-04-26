from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'username', 'email', 'kingdom_name']

class SuccessMessageSerializer(serializers.Serializer):
    status = serializers.CharField(allow_blank=True)
    token = serializers.CharField()


class ErrorMessageSerializer(serializers.Serializer):
    error = serializers.CharField(max_length=100)

class ErrorMessage:
    def __init__(self, error):
        self.error = error

class SuccessMessage:
    def __init__(self, status, token):
        self.status = status
        self.token = token
