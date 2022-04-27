from django.core.exceptions import PermissionDenied
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from rest_framework.views import APIView
from player.models import Player


class BaseView(APIView):
    
    def dispatch(self,request,*args, **kwargs):
        if is_authenticated(request.COOKIES):
            return super(BaseView, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied("Youre not logged in")

def is_authenticated(token):
    if "jwt" in token:
        return token_validation(token["jwt"])
    return None

def token_validation(token):
    try :
        player_id = jwt.decode(token,"secret", algorithms='HS256')["id"]
        return Player.objects.get(id=player_id)
    except InvalidSignatureError:
        return None
    except ExpiredSignatureError:
        return None
    except DecodeError:
        return None
