from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_agent = models.BooleanField(default=False)
    is_office = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    phone_no = PhoneNumberField()

    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name()

class Owner(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

class Client(models.Model):
    client = models.ForeignKey(Person, on_delete=models.CASCADE)


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    agent = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.user.first_name = self.agent.first_name
        self.user.last_name = self.agent.last_name
        self.user.email = self.agent.email
        self.user.save()

        return models.Model.save(self, *args, **kwargs)

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=30, null=False, default='Indore')
    state = models.CharField(max_length=30, null=False, default='Madhya Pradesh')
    country = models.CharField(max_length=30, null=False, default='India')

class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=20)
    zipcode = models.IntegerField(null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, default=1)

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=100, blank=True)

class Property(models.Model):

    PROPERTY_TYPE = [
        ('sale', 'sale'),
        ('rent', 'rent')
    ]

    DIRECTIONS = [
        ('north', 'north'),
        ('south', 'south'),
        ('west', 'west'),
        ('east', 'east')
    ]
    property_id = models.AutoField(primary_key=True)
    property_name = models.CharField(max_length=20, null=True, blank=True)
    property_image = models.ImageField('property_image', upload_to='images/', default='images/default.png', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    tag = models.CharField(max_length=4, choices=PROPERTY_TYPE, default='sale')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_bedrooms = models.IntegerField(default=1)
    no_of_bathrooms = models.IntegerField(default=1)
    floor = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    date_of_entry = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.property_name:            
            self.property_name = '{}-{} Nivas'.format(self.owner.owner.person_id, self.owner.owner.first_name)
            
        return models.Model.save(self, *args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['property_name'])
        ]
    def __str__(self):
        return '{}'.format(self.property_name)


class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    date_of_purchase = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        p = Property.objects.get(pk=self.property.property_id)
        p.is_available = False
        p.save()
        return models.Model.save(self, *args, **kwargs)

