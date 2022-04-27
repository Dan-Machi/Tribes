from http.cookies import SimpleCookie
import datetime
import jwt
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from rest_framework import status
from kingdom.models import Kingdom, Location
from .models import Player

class RegisterTestCase(APITestCase):
    def test_register(self):

        data1 = {
            "username": "player1",
            "email" : "player1@gmail.com",
            "password1" : "anything123",
            "password2" : "anything123"
        }

        data2 = {
            "username": "player2",
            "email": "player2@gmail.com",
            "password1" : "anything123",
            "password2" : "anything123",
            "kingdom_name" : "mega swag"
        }
        data3 = {
            "username": "player1",
            "email": "player3@gmail.com",
            "password1" : "anything123",
            "password2" : "anything123"
        }
        data4 = {
            "username": "player4",
            "email": "playergmail",
            "password1" : "anything123",
            "password2" : "anything123"
        }

        data5 = {
            "username": "player5",
            "email": "player5@gmail.com",
            "password1" : "anything123",
            "password2" : "anything12"
        }

        data6 = {
            "username": "",
            "email": "player6@gmail.com",
            "password1" : "anything123",
            "password2" : "anything123"
        }

        url = "http://127.0.0.1:8000/player/register/"

        response1 = self.client.post(url, data1)
        response2 = self.client.post(url, data2)
        response3 = self.client.post(url, data3)
        response4 = self.client.post(url, data4)
        response5 = self.client.post(url, data5)
        response6 = self.client.post(url, data6)

        self.assertEqual(response1.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)

class LoginTestCase(APITestCase):

    def test_login(self):
        Player.objects.create(username="username", password=make_password("password"))
        player = Player.objects.filter(username="username").first()
        self.assertEqual(Player.objects.get().username, "username")
        self.assertEqual(Player.objects.count(), 1)


        data1 = {
            "username": player.username,
            "password": "password"
        }

        data2 = {
            "username": "",
            "password": ""
        }

        data3 = {
            "username" : "username",
            "password" : "pswrd"
        }
        url = reverse("login")
        response1 = self.client.post(url, data1, format="json")
        response2 = self.client.post(url, data2, format="json")
        response3 = self.client.post(url, data3, format="json")

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth(self):
        Player.objects.create(username="Igor",password="password",
            email="email@email.com", kingdom_name="first")
        player = Player.objects.filter(username="Igor").first()
        payload = {
            "id": player.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            "iat": datetime.datetime.utcnow()
        }
        
        loc = Location.objects.create(x=0,y=0)
        Kingdom.objects.create(kingdom_name="first",
            location=loc,player=player)
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        self.client.cookies = SimpleCookie({"jwt":"abc"})
        url = reverse("auth")
        data1 = {"token":"token"}
        response1 = self.client.post(url,data1,format="json")
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

        self.client.cookies = SimpleCookie({"jwt":token})
        response1 = self.client.post(url,data1,format="json")
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

        data1 = {"token":token}
        response1 = self.client.post(url,data1,format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
