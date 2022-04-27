from __future__ import absolute_import, unicode_literals
from datetime import datetime

from django.db.models import F

from celery import shared_task

from building.models import Building

from .models import Kingdom, Resource


@shared_task
def resource_tick(resource_type):
    for kingdom in Kingdom.objects.all():

        building_type = None

        if resource_type == Resource.Type.F:
            building_type = Building.Type.FARM
        elif resource_type == Resource.Type.G:
            building_type = Building.Type.MINE

        addition = 0

        for building in Building.objects.filter(kingdom_id=kingdom.id,type=building_type):
            addition += building.level + building.level-1

        Resource.objects.filter(type=resource_type,kingdom_id=kingdom.id).update(
            amount=F('amount')+addition, updated_at = datetime.now().timestamp())
