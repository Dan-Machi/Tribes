from django.http import JsonResponse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from http.cookies import SimpleCookie
from .views import TroopView, TroopLeaderboard
from arctic_fox_tribes.conftest import *

def test_troop_no_exist_kingdom(db, token_1): # pylint: disable=unused-argument, invalid-name
    view = TroopView.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.get('troops')
    response = view(request, kingdom_id=10)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_troop_another_player_kingdom(db, kingdom_2, token_1): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            'error': 'This kingdom does not belong to authenticated player'
        }).content.decode()
    view = TroopView.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.get('troops')
    response = view(request, kingdom_id=2)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_data == expected_response_data

def test_kingdom_detail(db, kingdom_1, troop_1_p1, troop_3_p1, token_1): # pylint: disable=unused-argument, invalid-name, too-many-arguments
    view = TroopView.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.get('troops')
    response = view(request, kingdom_id=1)
    expected_response_data = JsonResponse(
        {
            "kingdom": {
            "kingdomId" : 1,
            "kingdomName" : "Babisovo",
            "ruler" : "roman",
            "population": 0,
            "location": {
                "coordinateX": 10,
                "coordinateY": -4
                }
            },
            "troops": [
            {
                "troop_type": "knight",
                "level": 1,
                "id": 9,
                "current_hp": "50.0",
                "started_at": 0,
                "finished_at": 0,
                "max_hp": 50.0,
                "attack": 50.0,
                "defence": 50.0,
                "speed": 10.0
            }, {
                "troop_type": "horseman",
                "level": 1,
                "id": 10,
                "current_hp": "50.0",
                "started_at": 0,
                "finished_at": 0,
                "max_hp": 75.0,
                "attack": 60.0,
                "defence": 50.0,
                "speed": 10.0
        }]}).content.decode()
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_response_data


def test_troop_leaderboard(db,get_all_kingdoms,get_all_troops):

    expected_response_data =JsonResponse({
        "results":[
            {
                "ruler" : "joe",
                "kingdom" : "Zemanovo",
                "troops_count" : 2,
                "points" : 4
            },
            {
                "ruler" : "roman",
                "kingdom" : "Babisovo",
                "troops_count" : 3,
                "points" : 3
            },
            {
                "ruler" : "permanent001",
                "kingdom" : "HajajBuvaj",
                "troops_count" : 0,
                "points" : 0
            }
            ]
        }).content.decode()

    factory = APIRequestFactory()
    view = TroopLeaderboard.as_view()
    request = factory.get('building_leaderboard')
    response = view(request)
    response_data = JsonResponse(response.data).content.decode()
    assert response_data == expected_response_data
    assert response.status_code == status.HTTP_200_OK
