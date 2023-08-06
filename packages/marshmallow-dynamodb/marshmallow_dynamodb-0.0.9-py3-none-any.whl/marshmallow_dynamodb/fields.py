"""Provides custom field for Marshmallow and he dumps a number."""
from datetime import datetime, timezone
from marshmallow.fields import DateTime
from decimal import Decimal


class DynamoDBDateTime(DateTime):
    """
    Custom field to dump a timestamp number.
    """

    def _serialize(self, value, attr, obj):
        if isinstance(value, datetime):
            return Decimal(int(value.replace(tzinfo=timezone.utc).timestamp()))  # Always remove microsecond/millisecond for DynamoDB(a.k.a
        # only seconds)
        if isinstance(value, str):
            try:
                return Decimal(int(datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).timestamp()))
            except(ValueError, AttributeError):
                raise self.fail('invalid')
        raise self.fail('invalid')

    def _deserialize(self, value, attr, data):
        if value:
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%dT%H:%M:%S')
            if isinstance(value, (float, int, Decimal)):
                if value >= 10000000000:
                    value = float(value) / 1000.0
                else:
                    value = int(value)
                return datetime.utcfromtimestamp(value).strftime('%Y-%m-%dT%H:%M:%S')
        return super(DateTime, self)._deserialize(value, attr, data)
