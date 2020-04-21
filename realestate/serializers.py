from rest_framework import serializers
from .models import *

class PropertySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Property
        fields = ('property_id', 'property_name')