from django.http.response import JsonResponse
from rest_framework import status
from .views import BuildingLeaderboard
from rest_framework.test import APIRequestFactory

from http.cookies import SimpleCookie

from .views import UpgradeBuilding
from arctic_fox_tribes.conftest import *

def test_building_leaderboard(db,get_all_kingdoms,get_all_farms):

    expected_response_data =JsonResponse({
        "results":[
            {
                "ruler" : "joe",
                "kingdom" : "Zemanovo",
                "buildings_count" : 3,
                "points" : 52
            },
            {
                "ruler" : "roman",
                "kingdom" : "Babisovo",
                "buildings_count" : 3,
                "points" : 36
            },
            {
                "ruler" : "permanent001",
                "kingdom" : "HajajBuvaj",
                "buildings_count" : 3,
                "points" : 25
            }
            ]
        }).content.decode()

    factory = APIRequestFactory()
    view = BuildingLeaderboard.as_view()
    request = factory.get('building_leaderboard')
    response = view(request)
    response_data = JsonResponse(response.data).content.decode()
    assert response_data == expected_response_data
    assert response.status_code == status.HTTP_200_OK


def test_upgrade_building_auth_player_enough_gold(db, kingdom_3, resource_g_p3, #pylint: disable=unused-argument, invalid-name
        farm_1_p3, token_3):
    expected_response_data = JsonResponse({
                                                "id": 9,
                                                "type": "1",
                                                "level": 2,
                                                "hp": 34,
                                                "started_at": int(datetime.datetime.now().timestamp()),
                                                "finished_at":  int(datetime.datetime.now().timestamp())
                                            }).content.decode()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_3})
    view = UpgradeBuilding.as_view()
    request = factory.put('upgrade_building')
    response = view(request, pk_kingdom=3, pk=9)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_response_data

def test_upg_building_no_auth_user(db, kingdom_2, token_1): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            "error": "This kingdom does not belong to authenticated player"
        }).content.decode()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    view = UpgradeBuilding.as_view()
    request = factory.put('upgrade_building')
    response = view(request, pk_kingdom=2, pk=1)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_data == expected_response_data

def test_upg_building_not_enough_gold(db, kingdom_3, farm_2_p3, token_3, resource_g_p3): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            "error": "You dont have enough gold to upgrade that!"
        }).content.decode()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_3})
    view = UpgradeBuilding.as_view()
    request = factory.put('upgrade_building')
    response = view(request, pk_kingdom=3, pk=10)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_data == expected_response_data

def test_upg_building_on_max_level(db, kingdom_3, farm_3_p3, token_3, resource_g_p3): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            "error": "Your building cannot be upgraded. It is already at max. level"
        }).content.decode()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_3})
    view = UpgradeBuilding.as_view()
    request = factory.put('upgrade_building')
    response = view(request, pk_kingdom=3, pk=11)
    response_data = JsonResponse(response.data, safe=False).content.decode()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_data == expected_response_data
