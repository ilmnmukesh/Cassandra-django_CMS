from django.db import models

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
import uuid

class CBorders(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4())
    oid= columns.UUID(required=True)
    cbid =columns.UUID(required=True)
    date = columns.Date(required=True)
    status=columns.Text()

