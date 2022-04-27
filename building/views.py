
import configparser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from kingdom.models import Kingdom, Resource

from arctic_fox_tribes.serializers import BuildingLeaderboardSerializer

from player.utils import BaseView, is_authenticated

from .models import Building
from .serializers import BuildingSerializer

class BuildingLeaderboard(APIView):

    def get(self,request):

        kingdoms = Kingdom.objects.all()
        serializer = BuildingLeaderboardSerializer(kingdoms,many=True).data
        serializer.sort(key=lambda x: x['points'],reverse=True)
        return Response(data={'results': serializer},status=status.HTTP_200_OK)

def choose_constant(name):
    config = configparser.ConfigParser()
    config.read_file(open("arctic_fox_tribes/config.ini"))
    section = name.upper()
    return dict(config.items(section))

class UpgradeBuilding(BaseView):
    def get_kingdom(self, pk_kingdom): #pylint: disable=invalid-name
        try:
            return Kingdom.objects.get(pk=pk_kingdom)
        except Kingdom.DoesNotExist:
            raise Http404

    def get_building(self, pk): #pylint: disable=invalid-name
        try:
            return Building.objects.get(pk=pk)
        except Building.DoesNotExist:
            raise Http404

    def put(self, request, pk_kingdom, pk): #pylint: disable=invalid-name
        kingdom = self.get_kingdom(pk_kingdom)
        if is_authenticated(request.COOKIES) == kingdom.player:
            building = self.get_building(pk)
            building_max_level = choose_constant(building.get_type_display())['max_level']
            if building.level < int(building_max_level):
                gold_needed = int(choose_constant(building.get_type_display())['upgrade_cost']
                        * building.level)
                gold_available = Resource.objects.get(kingdom_id=pk_kingdom, type=Resource.Type.G)
                if gold_available.amount >= gold_needed:
                    building.level += 1
                    building.save()
                    gold_available.amount -= gold_needed
                    gold_available.save()
                    building_serializer = BuildingSerializer(building)
                    return Response(building_serializer.data)
                content = {'error': 'You dont have enough gold to upgrade that!'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            content = {'error': 'Your building cannot be upgraded. It is already at max. level'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        content = {'error': 'This kingdom does not belong to authenticated player'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
