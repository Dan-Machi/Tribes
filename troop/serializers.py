from rest_framework import serializers
from troop.models import Troop, TroopType
from .utils import count_troop_property, get_value

class TroopSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    max_hp = serializers.SerializerMethodField()
    attack = serializers.SerializerMethodField()
    defence = serializers.SerializerMethodField()
    speed = serializers.SerializerMethodField()
    troop_type = serializers.SerializerMethodField()

    @classmethod
    def get_level(cls, troop):
        return troop.type.level
    @classmethod
    def get_max_hp(cls,troop):
        return count_troop_property(troop, "initial_hp", "hp_up")

    @classmethod
    def get_attack(cls,troop):
        return count_troop_property(troop, "initial_attack", "attack_up")

    @classmethod
    def get_defence(cls,troop):
        return count_troop_property(troop, "initial_defence", "defence_up")

    @classmethod
    def get_speed(cls,troop):
        return count_troop_property(troop, "initial_speed", "speed_up")

    @classmethod
    def get_troop_type(cls,troop):
        return get_value(troop.type.get_type_display(), "type")

    class Meta:
        model = Troop
        fields=["troop_type", "level" ,"id", "current_hp", "started_at",
         "finished_at", "max_hp", "attack", "defence", "speed"]

class TroopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TroopType
        fields=["type",]
