from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from player.utils import BaseView, is_authenticated
from kingdom.models import Kingdom, Resource
from kingdom.utils import create_troop
from kingdom.serializers import KingdomSerializer
from .models import TroopType, Troop
from .serializers import TroopSerializer
from .utils import get_value
from arctic_fox_tribes.serializers import TroopLeaderboardSerializer

class TroopView(BaseView):
    def post(self,request,kingdom_id):
        player = is_authenticated(request.COOKIES)
        kingdom = Kingdom.objects.get(pk=kingdom_id)
        if kingdom is not None and player.kingdom.id == kingdom.id:
            type = TroopType.objects.get(kingdom=kingdom, type=request.data["type"])
            gold = Resource.objects.get(kingdom=kingdom, type="G").amount
            required_gold = int(request.data["amount"])*type.level*int(get_value
                (request.data["type"], "cost"))

            if gold >= required_gold:
                response_data = create_troop(type=type,
                amount=request.data["amount"], kingdom=kingdom)
                Resource.objects.filter(kingdom=kingdom, type="G").update(amount=gold-required_gold)
                return Response(status=status.HTTP_200_OK, data = response_data)
            return Response(status=status.HTTP_400_BAD_REQUEST,
                data={"error":"You don't have enough gold to train all these units!"})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
            data={"error":"This kingdom does not belong to authenticated player"})

    def get(self, request, kingdom_id):
        if Kingdom.objects.filter(pk=kingdom_id).exists():
            kingdom = Kingdom.objects.get(pk=kingdom_id)
            if is_authenticated(request.COOKIES) == kingdom.player:
                troops = Troop.objects.filter(kingdom_id=kingdom.id)
                kingdom_serializer = KingdomSerializer(kingdom)
                troop_serializer = TroopSerializer(troops, many=True)
                data = {
                        'kingdom':kingdom_serializer.data,
                        'troops':troop_serializer.data,
                    }
                return Response(data)
            return Response(data={'error': 'This kingdom does not belong to authenticated player'},
            status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={'error': 'This kingdom does not exist'},
        status=status.HTTP_404_NOT_FOUND)
        
class TroopLeaderboard(APIView):
    def get(self,request):

        kingdoms = Kingdom.objects.all()
        serialized_data = TroopLeaderboardSerializer(kingdoms,many=True).data
        serialized_data.sort(key=lambda x: x['points'],reverse=True)

        return Response(data={'results' : serialized_data},status=status.HTTP_200_OK)
