import datetime
import jwt
import pytest
from player.models import Player
from kingdom.models import Kingdom, Location, Resource
from building.models import Building
from troop.models import TroopType, Troop

@pytest.fixture()
def player_1(db):  # pylint: disable=unused-argument, invalid-name
    yield Player.objects.create(id=1, username='roman', password='testing321')

@pytest.fixture()
def player_2(db):  # pylint: disable=unused-argument, invalid-name
    yield Player.objects.create(id=2, username='joe', password='testing321')

@pytest.fixture()
def player_3(db):  # pylint: disable= unused-argument, invalid-name
    yield Player.objects.create(id=3, username='permanent001', password='abcde')

@pytest.fixture()
def player_4(db):  # pylint: disable=unused-argument, invalid-name
    yield Player.objects.create(id=4, username='adam123', password='testing321')

@pytest.fixture()
def player_5(db):  # pylint: disable=unused-argument, invalid-name
    yield Player.objects.create(id=5, username='hanickaAmurko', password='testing321')

@pytest.fixture()
def location_1(db):  # pylint: disable=unused-argument, invalid-name
    yield Location.objects.create(x=10, y=-4)


@pytest.fixture()
def location_2(db):  # pylint: disable=unused-argument, invalid-name
    yield Location.objects.create(x=11, y=-5)


@pytest.fixture()
def location_3(db):  # pylint: disable=unused-argument, invalid-name
    yield Location.objects.create(x=12, y=-6)


@pytest.fixture()
def kingdom_1(db, player_1,location_1):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Kingdom.objects.create(id=1,kingdom_name='Babisovo', population=0,
                                 player=player_1,location=location_1)


@pytest.fixture()
def kingdom_2(db, player_2,location_2):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Kingdom.objects.create(id=2,kingdom_name='Zemanovo', population=0,
                                 player=player_2,location=location_2)


@pytest.fixture()
def kingdom_3(db, player_3,location_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Kingdom.objects.create(id=3,kingdom_name="HajajBuvaj", population=0,
                                 location=location_3, player=player_3)


@pytest.fixture()
def farm_1(db, kingdom_1):  # pylint: disable=unused-argument, redefined-outer-name, invalid-name
    yield Building.objects.create(id=1, type='1', level=1, hp=34,
                                  started_at=datetime.datetime.now().timestamp(),
                                  finished_at=datetime.datetime.now().timestamp(), kingdom_id=1)


@pytest.fixture()
def farm_2(db, kingdom_1):  # pylint: disable=unused-argument, redefined-outer-name, invalid-name
    yield Building.objects.create(id=2, type='1', level=10, kingdom_id=1)


@pytest.fixture
def farm_1_p1(db, kingdom_1):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=3,type=Building.Type.FARM, level=10, kingdom_id=kingdom_1.id)


@pytest.fixture
def farm_2_p1(db, kingdom_1):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=4,type=Building.Type.FARM, level=11, kingdom_id=kingdom_1.id)


@pytest.fixture()
def farm_3_p1(db, kingdom_1):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=5,type=Building.Type.FARM, level=15, kingdom_id=kingdom_1.id)


@pytest.fixture
def farm_1_p2(db, kingdom_2):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=6,type=Building.Type.FARM, level=9, kingdom_id=kingdom_2.id)


@pytest.fixture
def farm_2_p2(db, kingdom_2):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=7,type=Building.Type.FARM, level=31, kingdom_id=kingdom_2.id)

@pytest.fixture()
def farm_3_p2(db, kingdom_2):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=8,type=Building.Type.FARM, level=12, kingdom_id=kingdom_2.id)

@pytest.fixture
def farm_1_p3(db, kingdom_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=9,type=Building.Type.FARM, level=1,hp=34,
                                  started_at=datetime.datetime.now().timestamp(),
                                  finished_at=datetime.datetime.now().timestamp(),
                                  kingdom_id=kingdom_3.id)

@pytest.fixture
def farm_2_p3(db, kingdom_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=10,type=Building.Type.FARM, level=9, kingdom_id=kingdom_3.id)

@pytest.fixture()
def farm_3_p3(db, kingdom_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.create(id=11,type=Building.Type.FARM, level=15, kingdom_id=kingdom_3.id)

@pytest.fixture()
def get_all_kingdoms(db, kingdom_1, kingdom_2, kingdom_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Kingdom.objects.all()

@pytest.fixture()
def farms_kingdom_1(db, farm_1_p1, farm_2_p1, farm_3_p1):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.all()

@pytest.fixture()
def farms_kingdom_2(db, farm_1_p2, farm_2_p2, farm_3_p2):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.all()

@pytest.fixture()
def farms_kingdom_3(db, farm_1_p3, farm_2_p3, farm_3_p3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.all()

@pytest.fixture()
def get_all_farms(db, farms_kingdom_1, farms_kingdom_2, farms_kingdom_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Building.objects.all()

@pytest.fixture()
def resource_g_p1(db, kingdom_1):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Resource.objects.create(id=2, type=Resource.Type.G, amount=10, generation=3,
                                  updated_at=456, kingdom_id=kingdom_1.id)
@pytest.fixture()
def resource_f_p1(db, kingdom_1):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Resource.objects.create(id=1, type=Resource.Type.F, amount=20, generation=2,
                                  updated_at=1234, kingdom_id=kingdom_1.id)

@pytest.fixture()
def resource_g_p2(db, kingdom_2):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Resource.objects.create(id=2, type=Resource.Type.G, amount=1000, generation=3,
                                  updated_at=456, kingdom_id=kingdom_2.id)

@pytest.fixture()
def resource_f_p2(db, kingdom_2):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Resource.objects.create(id=1, type=Resource.Type.F, amount=20, generation=2,
                                  updated_at=1234, kingdom_id=kingdom_2.id)

@pytest.fixture()
def resource_g_p3(db, kingdom_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Resource.objects.create(id=2, type=Resource.Type.G, amount=1000, generation=3,
                                  updated_at=456, kingdom_id=kingdom_3.id)

@pytest.fixture()
def resource_f_p3(db, kingdom_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Resource.objects.create(id=1, type=Resource.Type.F, amount=20, generation=2,
                                  updated_at=1234, kingdom_id=kingdom_3.id)

@pytest.fixture()
def token_1(db, player_1):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    payload = {
        'id': player_1.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    yield jwt.encode(payload, 'secret', algorithm='HS256')

@pytest.fixture()
def token_2(db, player_2):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    payload = {
        'id': player_2.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    yield jwt.encode(payload, 'secret', algorithm='HS256')


@pytest.fixture()
def token_3(db, player_3):  # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    payload = {
        'id': player_3.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    yield jwt.encode(payload, 'secret', algorithm='HS256')

@pytest.fixture()
def troop_type_1_p1(db, kingdom_1): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield TroopType.objects.create(kingdom_id = kingdom_1.id, type="knight", level=1)

@pytest.fixture()
def troop_type_2_p1(db, kingdom_1): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield TroopType.objects.create(kingdom=kingdom_1,type="horseman", level=1)

@pytest.fixture()
def troop_type_1_p2(db, kingdom_2): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield  TroopType.objects.create(kingdom=kingdom_1,type="knight", level=2)

@pytest.fixture()
def troop_type_2_p2(db,kingdom_2): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield TroopType.objects.create(kingdom=kingdom_2, type="horseman",level=2)

@pytest.fixture()
def troop_1_p1(db,troop_type_1_p1,kingdom_1): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Troop.objects.create(kingdom=kingdom_1, type_id=troop_type_1_p1.id, 
        started_at=0, finished_at=0)

@pytest.fixture()
def troop_2_p1(db,troop_type_1_p1,kingdom_1): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Troop.objects.create(kingdom=kingdom_1,type_id=troop_type_1_p1.id,
        started_at=0, finished_at=0)

@pytest.fixture()
def troop_3_p1(db,troop_type_2_p1,kingdom_1): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Troop.objects.create(kingdom=kingdom_1,type_id=troop_type_2_p1.id,
        started_at=0, finished_at=0)

@pytest.fixture()
def troop_1_p2(db,troop_type_2_p2,kingdom_2): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Troop.objects.create(kingdom=kingdom_2,type_id=troop_type_2_p2.id)

@pytest.fixture()
def troop_2_p2(db,troop_type_2_p2,kingdom_2): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Troop.objects.create(kingdom=kingdom_2,type_id=troop_type_2_p2.id)

@pytest.fixture()
def get_troops_p1(db,troop_1_p1,troop_2_p1,troop_3_p1,kingdom_1):
    yield Troop.objects.filter(kingdom=kingdom_1)

@pytest.fixture()
def get_troops_p2(db,troop_1_p2,troop_2_p2, kingdom_2):
    yield Troop.objects.filter(kingdom=kingdom_2)

@pytest.fixture()
def get_all_troops(db,get_troops_p1,get_troops_p2): # pylint: disable=unused-argument, invalid-name, redefined-outer-name
    yield Troop.objects.all()