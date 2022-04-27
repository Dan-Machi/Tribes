from datetime import datetime

from django.db.models import F

from building.models import Building
from troop.models import Troop
from .models import Resource, Kingdom


def resource_tick(resource_type):

    for kingdom in Kingdom.objects.all():

        building_type = None

        if resource_type == 'F':
            building_type = Building.Type.FARM
        elif resource_type == 'G':
            building_type = Building.Type.MINE


        addition = 0

        for building in Building.objects.filter(kingdom_id=kingdom.id,type=building_type):
            addition += building.level + building.level-1

        Resource.objects.filter(type=resource_type,kingdom_id=kingdom.id).update(
            amount=F('amount')+addition, updated_at = datetime.now().timestamp())

        print(datetime.now(),kingdom.kingdom_name, resource_type,
                    Resource.objects.filter(kingdom_id=kingdom.id,type=resource_type).get().amount)

def troop_food_consumption():
    for kingdom in Kingdom.objects.all():
        consumption = 0

        for troop in Troop.objects.filter(kingdom_id=kingdom.id):
            consumption += troop.level

        Resource.objects.filter(kingdom_id=kingdom.id, type='F').update(
            amount=F('amount') - consumption, updated_at = datetime.now().timestamp())
