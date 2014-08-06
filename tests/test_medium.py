from models.medium import Medium, AdSize, AdUnit, AdPosition
from test_user import _add_team


def _add_medium(name):
    team = _add_team('testteam')
    medium = Medium(name, team)
    medium.add()
    return medium


def _add_size(width, height):
    size = AdSize(width, height)
    size.add()
    return size


def _add_unit(name, estimate_num, medium=None):
    size = _add_size(300, 50)
    medium = medium or _add_medium('testmedium')
    unit = AdUnit(name, '', size, '', 0, 1, medium, estimate_num)
    unit.add()
    return unit


def _add_position(name, medium=None):
    size = _add_size(300, 50)
    medium = medium or _add_medium('testmedium')
    position = AdPosition(name, '', size, 1, medium)
    position.add()
    return position


def test_medium(session):
    medium = _add_medium('testmedium')

    medium2 = Medium.get(medium.id)
    assert medium2.name == 'testmedium'


def test_size(session):
    size = _add_size(300, 50)

    size2 = AdSize.get(size.id)
    assert size2.width == 300
    assert size2.height == 50


def test_unit(session):
    unit = _add_unit('testunit', 300)

    unit2 = AdUnit.get(unit.id)
    assert unit2.name == 'testunit'
    assert unit2.estimate_num == 300


def test_position(session):
    position = _add_position('testposition')

    position2 = AdPosition.get(position.id)
    assert position2.name == 'testposition'
