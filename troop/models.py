from django.db import models
from django.utils.translation import gettext_lazy as _
from kingdom.models import Kingdom

class TroopType(models.Model):

    class Type(models.TextChoices):
        KNIGHT=0, _("knight")
        CAVALRY=1, _("cavalry")
        HORSEMAN=2, _("horseman")
        SPY=3, _("spy")
        SENATOR=4, _("senator")

    type = models.CharField(max_length=20, choices=Type.choices, null=True, blank=True)
    level = models.PositiveIntegerField(default = 1, null=True)
    kingdom = models.ForeignKey(Kingdom, related_name="kingdom",
    on_delete=models.SET_NULL, null=True)

class Troop(models.Model):
    type = models.ForeignKey(TroopType, related_name="troop_type",
    null=True, on_delete=models.SET_NULL)
    current_hp = models.DecimalField(null=True, max_digits=4, decimal_places=1, default=50)
    started_at = models.PositiveIntegerField(null=True)
    finished_at = models.PositiveIntegerField(null=True)
    kingdom = models.ForeignKey(Kingdom, related_name="kingdoms",
    on_delete=models.SET_NULL, null=True)
