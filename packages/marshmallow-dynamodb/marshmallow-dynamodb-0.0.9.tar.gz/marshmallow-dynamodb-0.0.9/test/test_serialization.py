from decimal import Decimal
from test.conftest import SomeSchema


def test_serialization_with_datetime(datetime_valid, datetime_epoch_seconds):
    data, errors = SomeSchema().dump({'field': datetime_valid})
    assert errors == {}
    assert data == {'field': Decimal(datetime_epoch_seconds)}
    assert isinstance(data['field'], Decimal)


def test_serialization_without_datetime():
    data, errors = SomeSchema().dump({'field': 123})
    assert errors == {'field': ['Not a valid datetime.']}
    assert data == {}
    assert data.get('field') is None


def test_serialization_with_string_datetime(datetime_string, datetime_epoch_seconds):
    data, errors = SomeSchema().dump({'field': datetime_string})
    assert errors == {}
    assert data == {'field': Decimal(datetime_epoch_seconds)}
    assert isinstance(data['field'], Decimal)
