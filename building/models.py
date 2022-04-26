
from django.utils.translation import gettext_lazy as _
from django.db import models
from kingdom.models import Kingdom

class Building(models.Model):
    class Type(models.TextChoices):
        TOWN_HALL = '0', _('Town Hall')
        FARM = '1', _('Farm')
        ACADEMY = '2', _('Academy')
        MINE = '3', _('Mine')

    type = models.CharField(max_length=20, choices=Type.choices, null=True, blank=False)
    level = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    started_at = models.IntegerField(default=0)
    finished_at = models.IntegerField(default=0)
    kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE, null=True, blank=False)
