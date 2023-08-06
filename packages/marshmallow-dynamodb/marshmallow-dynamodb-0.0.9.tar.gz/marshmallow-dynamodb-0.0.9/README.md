### DynamoDBFields:

Example usage:

```python
from datetime import datetime
from marshmallow import Schema
from marshmallow_dynamodb.fields import DynamoDBDateTime

class SchemaFixture(Schema):
    some_field = DynamoDBDateTime()
    
data, errors = SchemaFixture().load({'some_field': datetime.now().timestamp()})
# UnmarshalResult(data={'some_field': datetime.datetime(2018, 11, 22, 17, 37, 55)}, errors={})

SchemaFixture().dump(data)
# MarshalResult(data={'some_field': 1542915517.0}, errors={})
```