import datetime
import jwt

from django.shortcuts import render, redirect
from rest_framework.serializers import raise_errors_on_nested_writes
from .forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt


from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from kingdom.views import KingdomRegistrationView

from kingdom.models import Kingdom
from .forms import RegisterForm
from .models import Player
from .serializers import ErrorMessage, ErrorMessageSerializer, PlayerSerializer
from .utils import is_authenticated, BaseView, token_validation



@api_view(http_method_names=['POST', 'GET'])
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            player = form.save()
            if not player.kingdom_name:
                player.kingdom_name = player.username + "'s kingdom"
            player.save()
            serializer = PlayerSerializer(player)
            # return Response(serializer.data)
            # request.session['player_id'] = player.id
            player_id = serializer.data['id']
            return redirect('/kingdoms/register/{}'.format(player_id))
        return Response(status=400)
    form = RegisterForm()
    return render(request, 'register.html', context={'form':form})

class Login(APIView):
    @classmethod
    def post(cls, request):
        username = request.data["username"]
        password = request.data["password"]
        if not username or not password:
            return Response (data = ErrorMessageSerializer(ErrorMessage(
                "Field username and/or field password was empty!")).data,
                        status=status.HTTP_400_BAD_REQUEST)
        player = Player.objects.filter(username=username).first()
        if player is None or check_password(password, player.password) is False:
            return Response(data = ErrorMessageSerializer(ErrorMessage(
                "Username and/or password was incorrect!")).data,
                        status=status.HTTP_401_UNAUTHORIZED)
        payload = {
            "id": player.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'status': "ok",
            "token": token
        }
        response.status = status.HTTP_200_OK
        return response

class Auth(BaseView):
    @classmethod
    def post(cls,request):
        player1 = is_authenticated(request.COOKIES)
        if "token" in request.data and token_validation(request.data["token"]) is not None:
            player2 = token_validation(request.data["token"])
            if player1.id == player2.id:
                result_data = {}
                result_data["ruler"] = player1.id
                result_data["kingdomId"] = Kingdom.objects.filter(kingdom_name
                    =player1.kingdom_name).first().id
                result_data["kingdomName"] = player1.kingdom_name
                return Response (result_data, status.HTTP_200_OK)

            return Response (data = ErrorMessageSerializer(ErrorMessage(
            "Token doesnt belong to you!")).data,
                status=status.HTTP_400_BAD_REQUEST)

        return Response (data = ErrorMessageSerializer(ErrorMessage(
        "Invalid token!")).data,
               status=status.HTTP_400_BAD_REQUEST)
