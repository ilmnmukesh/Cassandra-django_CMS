from django.db import models
from django.contrib import  admin
# Create your models here.
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class MahalGallery(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    gallery_pic=columns.List(columns.Text)


class CateringBookingTemp(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)
    reg_type= columns.Text(primary_key=True)
    foodname=columns.Text(primary_key=True)
    veg_non = columns.Text()
    amount= columns.List(columns.Integer)

    class Meta:
        get_pk_field='id'

class MahalCalendar(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    cid = columns.UUID(primary_key=True)
    from_date= columns.Date(primary_key=True)
    to_date= columns.Date(primary_key=True)
    booker_name=columns.Text()
    amount=columns.Integer()
    rent_hr = columns.Integer()
    status=columns.Text(default='pending')

    class Meta:
        get_pk_field='id'
    