from rest_framework import serializers

from kingdom.models import Kingdom
from building.models import Building
from player.models import Player
from troop.models import Troop, TroopType


class BuildingLeaderboardSerializer(serializers.ModelSerializer):
    ruler = serializers.SerializerMethodField()
    kingdom = serializers.SerializerMethodField()
    buildings_count = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    class Meta:
        model = Kingdom
        fields = ['ruler', 'kingdom', 'buildings_count', 'points']
        depth = 1

    def get_ruler(self, instance):

        return Player.objects.get(id=instance.player_id).username

    def get_kingdom(self, instance):
        return instance.kingdom_name

    def get_buildings_count(self, instance):
        return Building.objects.filter(kingdom_id=instance.id).count()

    def get_points(self, instance):
        points = 0

        for building in Building.objects.filter(kingdom_id=instance.id):
            points += building.level

        return points


class TroopLeaderboardSerializer(serializers.ModelSerializer):
    ruler = serializers.SerializerMethodField()
    kingdom = serializers.SerializerMethodField()
    troops_count = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    class Meta:
        model = Kingdom
        fields = ['ruler', 'kingdom', 'troops_count', 'points']
        depth = 1

    def get_ruler(self, instance):
        return Player.objects.get(id=instance.player_id).username

    def get_kingdom(self, instance):
        return instance.kingdom_name

    def get_troops_count(self, instance):
        return Troop.objects.filter(kingdom_id=instance.id).count()

    def get_points(self, instance):
        points = 0

        for troop in Troop.objects.filter(kingdom_id=instance.id):
            points += TroopType.objects.get(id=troop.type_id).level
        return points


class KingdomLeaderboardSerializer(serializers.ModelSerializer):
    ruler = serializers.SerializerMethodField()
    kingdom = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    class Meta:
        model = Kingdom
        fields = ['ruler', 'kingdom', 'points']

    def get_ruler(self, instance):
        return Player.objects.get(id=instance.player_id).username

    def get_kingdom(self, instance):
        return instance.kingdom_name

    def get_points(self, instance):
        points = 0

        for building in Building.objects.filter(kingdom_id=instance.id):
            points += building.level

        for troop in Troop.objects.filter(kingdom_id=instance.id):
            points += TroopType.objects.get(id=troop.type_id).level

        return points
