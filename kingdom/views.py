import json
from django.http import Http404
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from troop.serializers import TroopSerializer
from troop.models import TroopType, Troop
from troop.utils import get_value

from player.utils import BaseView, is_authenticated
from building.models import Building
from building.serializers import BuildingSerializer
from .models import Kingdom, Location, Resource, Player
from .serializers import KingdomSerializer, ResourceSerializer
from arctic_fox_tribes.serializers import KingdomLeaderboardSerializer

class KingdomResources(BaseView):
    """
    Retrieve resource information for given kingdom.
    """
    def get_object(self, pk):
        try:
            return Kingdom.objects.get(pk=pk)
        except Kingdom.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        kingdom = self.get_object(pk)
        if is_authenticated(request.COOKIES) == kingdom.player:
            resources = Resource.objects.filter(kingdom_id=pk)
            kingdom_serializer = KingdomSerializer(kingdom)
            resources_serializer = ResourceSerializer(resources, many=True)
            return Response({
                'kingdom': kingdom_serializer.data,
                'resources': resources_serializer.data,
            })
        content = {'error': 'This kingdom does not belong to authenticated player'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

class KingdomRegistrationView(APIView):
    def get(self, request, pk):
        if not Kingdom.objects.filter(player_id=pk).exists():
            all_locations = []
            taken_locations = Location.objects.all()

            for a in range(-20, 21):
                for b in range(-20, 21):
                    all_locations.append(Location(x = a, y = b))

            for location in all_locations:
                for taken_location in taken_locations:
                    if location.x == taken_location.x and location.y == taken_location.y:
                        all_locations.remove(location)

            return render(request, 'kingdom_reqistration.html',
            context={'locations' : all_locations, 'player_id' : pk})
        return HttpResponseBadRequest('This player already has a kingdom registered')

    def get_player(self, pk):
        try:
            return Player.objects.get(pk=pk)
        except Player.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        selected_player = self.get_player(pk)
        my_list = json.loads(request.POST.get('location'))
        a = my_list[0]
        b = my_list[1]
        selected_location = Location.objects.create(x=a, y=b)
        kingdom = Kingdom.objects.create(location = selected_location,
            kingdom_name = selected_player.kingdom_name, player = selected_player)
        serializer = KingdomSerializer(kingdom)
        return Response(serializer.data)

def create_kingdom(request):
    data = request.json()
    player = data['uploaded'][0]
    kingdom = Kingdom()
    kingdom.name = player.kingdom_name
    kingdom.player = player

# Create your views here.
class KingdomList(BaseView):
    def get(self,request):

        kingdom_set = Kingdom.objects.all()

        if kingdom_set.count() > 0:
            kingdoms = KingdomSerializer(kingdom_set, many=True)

            return Response(data=
                {
                    'kingdoms': kingdoms.data
                }
            )
        return Response(data={"kingdoms": "No kingdoms available"})


class BuildingList(BaseView):
    @classmethod
    def get(cls, request, kingdom_id):
        player = is_authenticated(request.COOKIES)
        kingdom = Kingdom.objects.get(kingdom_name=player.kingdom_name)

        if kingdom is not None and kingdom.id == kingdom_id:
            result = {}
            result["kingdom"] = KingdomSerializer(kingdom).data
            result["buildings"] = BuildingSerializer(Building.objects.filter(kingdom=kingdom),
                            many=True).data
            return Response(data = result, status = status.HTTP_200_OK)

        return Response(data={'error': 'This kingdom does not belong to authenticated player'},
                        status=status.HTTP_401_UNAUTHORIZED)

class KingdomLeaderboard(APIView):
    def get(self, request):
        kingdoms = Kingdom.objects.all()
        serializer_data = KingdomLeaderboardSerializer(kingdoms,many=True).data

        serializer_data.sort(key=lambda x: x['points'],reverse=True)
        return Response(data={'response':serializer_data},status=status.HTTP_200_OK)

class TroopView(BaseView):
    def post(self,request,kingdom_id):
        player = is_authenticated(request.COOKIES)
        # kingdom = Kingdom.objects.filter(pk=kingdom_id).first()
        kingdom = Kingdom.objects.get(pk=kingdom_id)

        if kingdom is not None and player.kingdom.id == kingdom.id:

            type = TroopType.objects.get(kingdom_id=kingdom.id, type=request.data["type"])
            gold = Resource.objects.get(kingdom=kingdom, type="G").amount
            required_gold = int(request.data["amount"])*type.level*int(get_value
            (request.data["type"], "cost"))

            if gold >= required_gold:
                response_data = create_troop(type=type,
                amount=request.data["amount"], kingdom=kingdom)
                Resource.objects.filter(kingdom=kingdom, type="G").update(amount=gold-required_gold)
                return Response(status=status.HTTP_200_OK, data = response_data)

class KingdomDetail(BaseView):
    def get_object(self, pk):
        try:
            return Kingdom.objects.get(pk=pk)
        except Kingdom.DoesNotExist:
            raise Http404
            
    #rename kingdom
    def put(self, request, pk, format=None):
        kingdom = self.get_object(pk)
        if is_authenticated(request.COOKIES) == kingdom.player:
            serializer = KingdomSerializer(kingdom, data=request.data,
                    fields=['kingdomId', 'kingdomName'], partial=True)
            if serializer.is_valid() and 'kingdomName' in request.data:
                serializer.save()
                return Response(serializer.data)
            if 'kingdomName' not in request.data:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.data['kingdomName'] == '':
                content = {'error': 'Field kingdomName was empty!'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        content = {'error': 'This kingdom does not belong to authenticated player'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    #kingdom detail
    def get(self, request, kingdom_id):
        if Kingdom.objects.filter(pk=kingdom_id).exists():
            kingdom = Kingdom.objects.get(pk=kingdom_id)
            if is_authenticated(request.COOKIES) == kingdom.player:
                buildings = Building.objects.filter(kingdom_id=kingdom.id)
                troops = Troop.objects.filter(kingdom_id=kingdom.id)
                resources = Resource.objects.filter(kingdom_id=kingdom.id)
                kingdom_serializer = KingdomSerializer(kingdom)
                resource_serializer = ResourceSerializer(resources, many=True)
                building_serializer = BuildingSerializer(buildings, many=True)
                troop_serializer = TroopSerializer(troops, many=True)
                data = {
                    'kingdom':kingdom_serializer.data,
                    'resources':resource_serializer.data,
                    'buildings':building_serializer.data,
                    'troops':troop_serializer.data,
                }
                return Response(data)
            return Response(data={'error': 'This kingdom does not belong to authenticated player'},
            status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={'error': 'This kingdom does not exist'},
        status=status.HTTP_404_NOT_FOUND)
