from django.db import models

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from django_cassandra_engine.models import DjangoCassandraModel
import uuid

class SignupCustomer(DjangoCassandraModel):
    id=columns.UUID(primary_key=True,default=uuid.uuid4())
    name = columns.Text(max_length=30)
    email = columns.Text( max_length=40)
    age= columns.Integer()
    gender= columns.Text(max_length=10)
    address = columns.Map(columns.Text,columns.Text)
    prof_img = columns.Text(max_length=100)
    ph_numb = columns.BigInt()
    password = columns.Text()

    def __str__(self):
        return self.email
    
    class Meta:
        get_pk_field='email'

class SignupCateringBoy(DjangoCassandraModel):
    id=columns.UUID(primary_key=True,default=uuid.uuid4())
    name = columns.Text(max_length=30)
    email = columns.Text(max_length=40)
    age= columns.Integer()
    address = columns.Map(columns.Text,columns.Text)
    prof_img = columns.Text(max_length=100)
    ph_numb = columns.BigInt()
    password = columns.Text()

    def __str__(self):
        return self.email
    
    class Meta:
        get_pk_field='email'

class SignupCateringService(DjangoCassandraModel):
    id=columns.UUID(primary_key=True,default=uuid.uuid1())
    name = columns.Text(max_length=30)
    manager = columns.Text(max_length=30)
    email = columns.Text(max_length=40)
    experience= columns.Integer()
    address = columns.Map(columns.Text,columns.Text)
    prof_img = columns.Text(max_length=100)
    contact = columns.List(columns.BigInt)
    password = columns.Text()

    def __str__(self):
        return self.email
    
    class Meta:
        get_pk_field='email'

class SignupMahalService(DjangoCassandraModel):
    id=columns.UUID(primary_key=True,default=uuid.uuid1())
    name = columns.Text(max_length=30)
    manager = columns.Text(max_length=30)
    email = columns.Text(max_length=40)
    build_yr = columns.Integer()
    address = columns.Map(columns.Text,columns.Text)
    prof_img = columns.Text(max_length=100)
    contact = columns.List(columns.BigInt)
    password = columns.Text()
    rent_amount=columns.Integer()

    def __str__(self):
        return self.email

    class Meta:
        get_pk_field='email'

class UserEmail(DjangoCassandraModel):
    email = columns.Text(primary_key=True, max_length=40)
    service = columns.Text(max_length=40)

    class Meta:
        get_pk_field='email'
    
