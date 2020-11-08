from django.db import models

# Create your models here.
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
import uuid
"""
class CateringBooking(DjangoCassandraModel):
    cbkid = columns.UUID(primary_key=True, default=uuid.uuid4)
    csid=columns.UUID(required=True)
    cusid=columns.UUID(required=True)
    date=columns.Date(required=True)
    foodlistid=columns.UUID()
    status = columns.Text()

class MahalBooking(DjangoCassandraModel):
    mbkid = columns.UUID(primary_key=True, default=uuid.uuid4)
    mid=columns.UUID(required=True)
    cusid=columns.UUID(required=True)
    date=columns.Date(required=True)
    status = columns.Text()

"""
class CustomerBookingTemp(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)
    reg_type= columns.Text(primary_key=True)
    foodname=columns.Text(primary_key=True)
    veg_non = columns.Text()
    amount= columns.List(columns.Integer)

    class Meta:
        get_pk_field='id'