
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from player.models import Player

class Location(models.Model):
    x = models.IntegerField(validators=[MinValueValidator(-20),
                    MaxValueValidator(20)],blank=False, null=True)
    y = models.IntegerField(validators=[MinValueValidator(-20),
                    MaxValueValidator(20)],blank=False, null=True)

class Kingdom(models.Model):
    kingdom_name = models.CharField(max_length=50, blank=False, null=True)
    population = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    player = models.OneToOneField(Player, on_delete=models.SET_NULL, null=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.kingdom_name)


class Resource(models.Model):

    class Type(models.TextChoices):
        F = 'F', _('food')
        G = 'G', _('gold')

    type = models.CharField(max_length=1, choices=Type.choices)
    amount = models.PositiveIntegerField(default=0,blank=False, null=True)
    generation = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],
                    blank=False, null=True)
    updated_at = models.IntegerField(default=0)
    kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE, blank=False, null=True)
