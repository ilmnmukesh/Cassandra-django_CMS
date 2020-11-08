from django.db import models

from cassandra.cqlengine import columns
import uuid, datetime, time
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.util import Date, Time

class CateringBoyOrder(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    cid= columns.UUID()
    venue = columns.Map(columns.Text(),columns.Text())
    amount = columns.Integer(default=300)
    catboy_max=columns.Integer(default=0)
    timing = columns.Time(default=Time('19:00:00'))
    date= columns.Date(default=Date(datetime.date.today().strftime("%Y-%m-%d")))
    count=columns.Integer(default=0)

class CateringServiceOrder(DjangoCassandraModel):
    receiver_id= columns.UUID(primary_key=True)
    booker_id=columns.UUID(primary_key=True)
    reg_type=columns.Text(primary_key=True)
    date= columns.Date(primary_key=True , default=Date(datetime.date.today().strftime("%Y-%m-%d")))
    amount = columns.Integer()
    plates=columns.Integer()
    foodlist=columns.Map(columns.Text, columns.List(columns.Text))
    address=columns.Text()
    status=columns.Text()

    class Meta:
        get_pk_field='receiver_id'

class CateringGallery(DjangoCassandraModel):
    id= columns.UUID(primary_key=True)
    gallery_pic = columns.List(columns.Text())

class CateringBreakfast(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    foods = columns.Map(columns.Text, columns.List(columns.Integer))

class CateringLunchVeg(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    foods = columns.Map(columns.Text, columns.List(columns.Integer))

class CateringLunchNonveg(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    foods = columns.Map(columns.Text,columns.List(columns.Integer))

class CateringDinnerVeg(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    foods = columns.Map(columns.Text,columns.List(columns.Integer))

class CateringDinnerNonveg(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    foods = columns.Map(columns.Text, columns.List(columns.Integer))