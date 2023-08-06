from decimal import Decimal
from test.conftest import SomeSchema


def test_deserialization_with_datetime(datetime_valid, datetime_string):
    data, errors = SomeSchema().load({'field': datetime_valid})
    assert errors == {}
    assert data == {'field': datetime_string}
    assert isinstance(data['field'], str)


def test_deserialization_with_number_types(datetime_epoch_miliseconds, datetime_epoch_seconds, datetime_string):
    data, errors = SomeSchema().load({'field': datetime_epoch_seconds})
    assert errors == {}
    assert data == {'field': datetime_string}
    assert isinstance(data['field'], str)

    data, errors = SomeSchema().load({'field': datetime_epoch_miliseconds})
    assert errors == {}
    assert data == {'field': datetime_string}
    assert isinstance(data['field'], str)

    data, errors = SomeSchema().load({'field': Decimal(datetime_epoch_miliseconds)})
    assert errors == {}
    assert data == {'field': datetime_string}
    assert isinstance(data['field'], str)


def test_deserialization_with_datetime_string(datetime_string):
    data, errors = SomeSchema().load({'field': datetime_string})
    assert errors == {}
    assert data == {'field': datetime_string}
    assert isinstance(data['field'], str)
