from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class PropertyForm(forms.ModelForm):
    
    class Meta:
        model = Property
        fields = "__all__"

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = "__all__"

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        

