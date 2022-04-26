from datetime import datetime
from http.cookies import SimpleCookie
from django.http import JsonResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from troop.views import TroopView
from .cron import resource_tick
from .models import Resource
from .views import KingdomList, KingdomResources, KingdomDetail, KingdomLeaderboard
from .tasks import resource_tick
from arctic_fox_tribes.conftest import *

def test_get_kingdom_resources_players_kingdom(db, kingdom_3, resource_g_p3, resource_f_p3,location_1, token_3): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
                                            "kingdom": {
                                                "kingdomId": 3,
                                                "kingdomName": "HajajBuvaj",
                                                "ruler": "permanent001",
                                                "population": 0,
                                                "location": {
                                                    "coordinateX": 12,
                                                    "coordinateY": -6
                                                }
                                            },
                                            "resources": [
                                                {
                                                    "type": "gold",
                                                    "amount": 1000,
                                                    "generation": 3,
                                                    "updatedAt": 456
                                                },
                                                {
                                                    "type": "food",
                                                    "amount": 20,
                                                    "generation": 2,
                                                    "updatedAt": 1234
                                                },

                                            ]
                                        }
                                        ).content.decode()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_3})
    view = KingdomResources.as_view()
    request = factory.get('kingdom_resources')
    response = view(request, pk=3)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_response_data

def test_get_kingdom_resources_other_player_kingdom(db, kingdom_2, token_1): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            "error": "This kingdom does not belong to authenticated player"
        }).content.decode()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    view = KingdomResources.as_view()
    request = factory.get('kingdom_resources')
    response = view(request, pk=2)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_data == expected_response_data

def test_get_kingdom_resources_no_exist_kingdom(db, token_1): # pylint: disable=unused-argument, invalid-name
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    view = KingdomResources.as_view()
    request = factory.get('kingdom_resources')
    response = view(request, pk=10)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_rename_own_kingdom(db, kingdom_1, token_1): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            'kingdomId': 1, 'kingdomName': 'Vaclavovo'
        }).content.decode()
    factory = APIRequestFactory()
    view = KingdomDetail.as_view()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.put('detail', {'kingdomName': 'Vaclavovo'})
    response = view(request, pk=1)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_response_data

def test_rename_own_kingdom_with_blank_name(db, kingdom_1, token_1): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            'error': 'Field kingdomName was empty!'
        }).content.decode()
    view = KingdomDetail.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.put('detail', {'kingdomName': ''})
    response = view(request, pk=1)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_data == expected_response_data

def test_rename_not_owned_kingdom(db, kingdom_2, token_1): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            'error': 'This kingdom does not belong to authenticated player'
        }).content.decode()
    view = KingdomDetail.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.put('detail', {'kingdomName': ''})
    response = view(request, pk=2)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_data == expected_response_data

def test_rename_no_exist_kingdom(db, token_1): # pylint: disable=unused-argument, invalid-name
    view = KingdomDetail.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.put('detail', {'kingdomName': 'Vaclavovo'})
    response = view(request, pk=10)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_rename_kingdom_wrong_request(db, kingdom_1, token_1): # pylint: disable=unused-argument, invalid-name
    view = KingdomDetail.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.put('detail', {'blabla': 'chrchr'})
    response = view(request, pk=1)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_for_zero_kingdom(db,token_1): # pylint: disable=unused-argument, invalid-name
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    view = KingdomList.as_view()
    request = factory.get('detail')
    response = view(request)
    assert response.data == {"kingdoms": "No kingdoms available"}

def test_kingdom_detail(db, kingdom_1, resource_g_p1, resource_f_p1, farm_1_p1, # pylint: disable=unused-argument, invalid-name, too-many-arguments
        farm_2_p1, troop_1_p1, troop_3_p1, token_1): # pylint: disable=unused-argument, invalid-name, too-many-arguments
    view = KingdomDetail.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.get('detail')
    response = view(request, kingdom_id=1)
    expected_response_data = JsonResponse(
        {
            "kingdom": {
            "kingdomId" : 1,
            "kingdomName" : "Babisovo",
            "ruler" : "roman",
            "population": 21,
            "location": {
                "coordinateX": 10,
                "coordinateY": -4
                }
            },
            "resources": [
            {
                "type" : "gold",
                "amount": 10,
                "generation": 3,
                "updatedAt": 456
            }, {
                "type" : "food",
                "amount": 20,
                "generation": 2,
                "updatedAt": 1234
            }
            ],
            "buildings": [
            {
                "id" : 3,
                "type" : "1",
                "level": 10,
                "hp": 0,
                "started_at": 0,
                "finished_at": 0
            },
            {
                "id" : 4,
                "type" : "1",
                "level": 11,
                "hp": 0,
                "started_at": 0,
                "finished_at": 0
            }
            ],
            "troops": [
            {
                "troop_type": "knight",
                "level": 1,
                "id": 1,
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
                "id": 2,
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

def test_detail_no_exist_kingdom(db, token_1): # pylint: disable=unused-argument, invalid-name
    view = KingdomDetail.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.get('detail')
    response = view(request, kingdom_id=10)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_detail_another_player_kingdom(db, kingdom_2, token_1): # pylint: disable=unused-argument, invalid-name
    expected_response_data = JsonResponse({
            'error': 'This kingdom does not belong to authenticated player'
        }).content.decode()
    view = KingdomDetail.as_view()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    request = factory.get('detail')
    response = view(request, kingdom_id=2)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_data == expected_response_data

def test_for_one_kingdom(db,player_1,kingdom_1,token_1): # pylint: disable=unused-argument, invalid-name
    url_for_test = 'kingdoms'
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    view = KingdomList.as_view()
    request = factory.get(url_for_test)
    response = view(request)
    expected_response_data = JsonResponse({'kingdoms':
        [{'kingdomId':1,
          'kingdomName':'Babisovo',
          'ruler':'roman',
          'population':0,
          'location':{
              'coordinateX': 10,
              'coordinateY': -4
              }
          }]}).content.decode()
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_response_data


def test_for_endpoint(db, kingdom_1,kingdom_2,player_1,player_2,token_1): # pylint: disable=unused-argument, invalid-name
    url_for_test = 'kingdoms'
    expected_response_data = JsonResponse({
                "kingdoms": [
                    {
                        "kingdomId": 1,
                        "kingdomName": "Babisovo",
                        "ruler": "roman",
                        "population": 0,
                        "location": {
                            "coordinateX": 10,
                            "coordinateY": -4
                        }
                    },
                    {
                        "kingdomId": 2,
                        "kingdomName": "Zemanovo",
                        "ruler": "joe",
                        "population": 0,
                        "location": {
                            "coordinateX": 11,
                            "coordinateY": -5
                        }
                    }
                ]
            }
            ).content.decode()
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({'jwt':token_1})
    view = KingdomList.as_view()
    request = factory.get(url_for_test)
    response = view(request)
    response_data = JsonResponse(response.data).content.decode()
    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_response_data

def test_for_create_troop(db,player_1,player_2, kingdom_1,
    kingdom_2, resource_g_p1, troop_type_1_p1, token_1): # pylint: disable=unused-argument, invalid-name, too-many-arguments
    sample_request1 = {
        "type":"knight",
        "amount":1
    }
    sample_request2 = {
        "type":"knight",
        "amount":10
    }
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie({"jwt":token_1})
    view = TroopView.as_view()
    url = reverse('troops', args=[kingdom_1.id])
    request = factory.post(url, sample_request1)
    response = view(request, kingdom_id=kingdom_1.id)
    assert response.status_code == status.HTTP_200_OK
    request2 = factory.post(url,sample_request2)
    response2 = view(request2, kingdom_id=kingdom_1.id)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    request3 = factory.post(url, sample_request1)
    response3 = view(request3, kingdom_id=kingdom_2.id)
    assert response3.status_code == status.HTTP_401_UNAUTHORIZED

def test_resource_tick_lvl_1(db,farm_1_p3,kingdom_3,resource_f_p3):# pylint: disable=unused-argument, invalid-name, too-many-arguments
    resource_tick('F')
    kingdom_food = Resource.objects.filter(kingdom_id=kingdom_3.id, type='F').get()
    assert kingdom_food.amount == 21
    assert kingdom_food.updated_at == (int)(datetime.datetime.now().timestamp())

def test_resource_tick_lvl_2(db,farm_3_p3,kingdom_3,resource_f_p3):# pylint: disable=unused-argument, invalid-name, too-many-arguments
    resource_tick('F')
    kingdom_food = Resource.objects.filter(kingdom_id=kingdom_3.id, type='F').get()
    assert kingdom_food.amount == 49

def test_kingdom_leaderboard(db,get_all_kingdoms,get_all_farms,get_all_troops):# pylint: disable=unused-argument, invalid-name, too-many-arguments
    expected_response = JsonResponse({"response": [
                            {
                                 "ruler": "joe",
                                 "kingdom": "Zemanovo",
                                 "points": 56
                            },
                            {
                                "ruler": "roman",
                                "kingdom": "Babisovo",
                                "points": 39
                            },
                            {
                                "ruler":"permanent001",
                                "kingdom": "HajajBuvaj",
                                "points": 25
                            }
                            ]}).content.decode()

    factory = APIRequestFactory()
    view = KingdomLeaderboard.as_view()
    request = factory.get('leaderboards/kingdoms')
    response = view(request)
    response_data = JsonResponse(response.data).content.decode()
    assert response_data == expected_response
    assert status.HTTP_200_OK == response.status_code
