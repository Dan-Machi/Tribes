from troop.serializers import TroopSerializer
from troop.models import Troop


def create_troop(type, amount, kingdom):
    result = []
    for _ in range (0,int(amount)):
        troop = Troop.objects.create(type=type, kingdom=kingdom)
        result.append(TroopSerializer(troop).data)
    return result
