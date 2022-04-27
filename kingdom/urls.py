from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import KingdomResources, KingdomRegistrationView, KingdomList, BuildingList
from building.views import UpgradeBuilding
from troop.views import TroopView
from .views import KingdomResources, KingdomList, BuildingList
from .views import KingdomDetail, KingdomRegistrationView

urlpatterns = [
    path('<int:pk>/resources/', KingdomResources.as_view()),
    path('register/<pk>/', KingdomRegistrationView.as_view(), name='register_kingdom'),
    path('<int:pk>/resources/', KingdomResources.as_view(), name='kingdom_resources'),
    path('', KingdomList.as_view(), name='kingdoms'),
    path('<int:kingdomId>/buildings/', BuildingList.as_view(), name='buildings'),
    path('<int:kingdom_id>/', KingdomDetail.as_view(), name='detail'),
    path('<int:kingdom_id>/troops/',TroopView.as_view(), name="troops"),
    path('<int:pk_kingdom>/buildings/<int:pk>/', UpgradeBuilding.as_view(), name='upgrade_building'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
