from django.contrib.auth.forms import UserCreationForm
from .models import Player

class RegisterForm(UserCreationForm):
    class Meta:
        model = Player
        fields = ('username', 'email', 'kingdom_name')
