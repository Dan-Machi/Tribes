from datetime import datetime
from django.db.models import F

from kingdom.models import Kingdom, Resource
from .models import Troop

def consume_food():
    for kingdom in Kingdom.objects.all():

        total_consumption = 0

        for troop in Troop.objects.filter(kingdom_id=kingdom.id):

            total_consumption += troop.level

        Resource.objects.filter(kingdom_id=kingdom.id,type='F').update(
            amount=F('amount') - total_consumption, updated_at= datetime.now().timestamp())
