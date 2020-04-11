from django import forms
from .models import *

class PropertyForm(forms.ModelForm):
    
    class Meta:
        model = Property
        fields = "__all__"

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = "__all__"